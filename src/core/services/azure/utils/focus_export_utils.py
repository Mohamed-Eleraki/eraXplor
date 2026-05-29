"""
Utility functions for configuring Azure FOCUS exports.

This module contains helper functions for:
- Azure authentication
- Building Azure Cost Management export payloads
- Creating scheduled FOCUS exports in Parquet format
"""

from datetime import UTC, datetime, timedelta
from typing import Any
import requests
from api.config import settings
from src.core.services.utils.common_shared_utils import (
    get_access_token,
)


def _build_scope(
    billing_account_id: str,
    billing_profile_id: str,
) -> str:
    """
    Build the Azure billing scope path for Cost Management exports.

    Args:
        billing_account_id (str): Azure billing account identifier.
        billing_profile_id (str): Azure billing profile identifier.

    Returns:
        str: Azure billing scope path used in export API requests.
    """
    return (
        f"/providers/Microsoft.Billing/"
        f"billingAccounts/{billing_account_id}"
        f"/billingProfiles/{billing_profile_id}"
    )


def _build_storage_resource_id(
    subscription_id: str,
    resource_group_name: str,
    storage_account_name: str,
) -> str:
    """
    Build the Azure Storage Account resource ID.

    Args:
        subscription_id (str): Azure subscription ID.
        resource_group_name (str): Resource group containing storage account.
        storage_account_name (str): Azure Storage Account name.

    Returns:
        str: Full Azure resource ID for the storage account.
    """
    return (
        f"/subscriptions/{subscription_id}"
        f"/resourceGroups/{resource_group_name}"
        f"/providers/Microsoft.Storage/"
        f"storageAccounts/{storage_account_name}"
    )


def _get_arm_headers(token: str) -> dict[str, str]:
    """Build headers for Azure Resource Manager API calls."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _fetch_arm_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    """Send a GET request to Azure ARM and return parsed JSON."""
    response = requests.get(url=url, headers=headers, timeout=60)
    if not response.ok:
        raise RuntimeError(
            f"Azure ARM request failed: {response.status_code} - {response.text}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError("Azure ARM response returned invalid JSON.") from exc


def get_billing_accounts() -> list[dict[str, Any]]:
    """Return billing accounts available to the authenticated Azure identity."""
    token = get_access_token()
    url = (
        f"{settings.AZURE_MANAGEMENT_BASE_URL}"
        "/providers/Microsoft.Billing/billingAccounts"
        "?api-version=2020-05-01"
    )
    data = _fetch_arm_json(url, _get_arm_headers(token))
    return data.get("value", [])


def get_billing_profiles(billing_account_id: str) -> list[dict[str, Any]]:
    """Return billing profiles for a given Azure billing account."""
    token = get_access_token()
    url = (
        f"{settings.AZURE_MANAGEMENT_BASE_URL}"
        f"/providers/Microsoft.Billing/billingAccounts/{billing_account_id}"
        "/billingProfiles?api-version=2020-05-01"
    )
    data = _fetch_arm_json(url, _get_arm_headers(token))
    return data.get("value", [])


def get_default_billing_account_and_profile_ids() -> dict[str, str]:
    """Fetch the first available billing account and profile IDs for the authenticated credential."""
    accounts = get_billing_accounts()
    if not accounts:
        raise RuntimeError(
            "No Azure billing accounts were found for the authenticated identity."
        )

    billing_account = accounts[0]
    billing_account_id = billing_account.get("name")
    if not billing_account_id:
        raise RuntimeError(
            "Billing account response missing required 'name' field."
        )

    profiles = get_billing_profiles(billing_account_id)
    if not profiles:
        raise RuntimeError(
            f"No billing profiles found for billing account '{billing_account_id}'."
        )

    billing_profile = profiles[0]
    billing_profile_id = billing_profile.get("name")
    if not billing_profile_id:
        raise RuntimeError(
            "Billing profile response missing required 'name' field."
        )

    return {
        "billing_account_id": billing_account_id,
        "billing_profile_id": billing_profile_id,
    }


def build_export_payload(
    storage_resource_id: str,
    container_name: str,
    folder_name: str,
) -> dict[str, Any]:
    """
    Build the request payload for Azure FOCUS export creation.

    The payload configures:
    - FOCUS cost dataset
    - Daily export schedule
    - Parquet output format
    - Destination storage container and folder

    Args:
        storage_resource_id (str): Azure Storage Account resource ID.
        container_name (str): Blob container name.
        folder_name (str): Root folder path for exported files.

    Returns:
        dict[str, Any]: JSON payload for Azure export API request.
    """
    start_date = (
        datetime.now(UTC) + timedelta(days=1)
    ).strftime("%Y-%m-%dT00:00:00Z")

    end_date = "2030-01-01T00:00:00Z"

    return {
        "location": "global",
        "identity": {
            "type": "SystemAssigned",
        },
        "properties": {
            "definition": {
                "type": "FocusCost",
                "timeframe": "MonthToDate",
                "dataset": {
                    "granularity": "Daily",
                    "configuration": {
                        "dataVersion": "1.0",
                    },
                },
            },
            "deliveryInfo": {
                "destination": {
                    "resourceId": storage_resource_id,
                    "container": container_name,
                    "rootFolderPath": folder_name,
                }
            },
            "format": "Parquet",
            "partitionData": True,
            "schedule": {
                "status": "Active",
                "recurrence": "Daily",
                "recurrencePeriod": {
                    "from": start_date,
                    "to": end_date,
                },
            },
        },
    }


def create_focus_export(
    billing_account_id: str,
    billing_profile_id: str,
    subscription_id: str,
    resource_group_name: str,
    storage_account_name: str,
    container_name: str,
    folder_name: str,
    export_name: str = "focus-cost-export",
) -> dict[str, Any]:
    """
    Create an Azure Cost Management FOCUS export.

    This function authenticates to Azure, builds the required export
    configuration, and creates a scheduled FOCUS export that writes
    Parquet files into the specified Azure Storage container.

    Args:
        billing_account_id (str): Azure billing account identifier.
        billing_profile_id (str): Azure billing profile identifier.
        subscription_id (str): Azure subscription ID.
        resource_group_name (str): Resource group containing storage account.
        storage_account_name (str): Destination storage account name.
        container_name (str): Blob container name.
        folder_name (str): Folder path inside container.
        export_name (str, optional): Export job name.
            Defaults to "focus-cost-export".

    Returns:
        dict[str, Any]: Result containing:
            - status_code (int): HTTP response code.
            - data (dict[str, Any]): Parsed API response.

    Raises:
        RuntimeError: If Azure API request fails.
    """
    print("Authenticating to Azure...")
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    scope = _build_scope(
        billing_account_id,
        billing_profile_id,
    )

    storage_resource_id = _build_storage_resource_id(
        subscription_id,
        resource_group_name,
        storage_account_name,
    )

    payload = build_export_payload(
        storage_resource_id,
        container_name,
        folder_name,
    )

    url = (
        f"{settings.AZURE_MANAGEMENT_BASE_URL}{scope}"
        f"/providers/Microsoft.CostManagement/"
        f"exports/{export_name}"
        f"?api-version={settings.AZURE_COST_API_VERSION}"
    )

    print("Creating FOCUS export...")

    response = requests.put(
        url=url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"FOCUS export failed: "
            f"{response.status_code} - {response.text}"
        )

    print("FOCUS export created successfully.")

    try:
        data = response.json()
    except ValueError:
        data = {"message": response.text}

    return {
        "status_code": response.status_code,
        "data": data,
    }
