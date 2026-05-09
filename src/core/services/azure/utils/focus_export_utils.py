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
from azure.identity import DefaultAzureCredential
from api.config import settings



def get_access_token() -> str:
    """
    Retrieve an Azure access token using DefaultAzureCredential.

    This function authenticates against Azure Active Directory and
    requests a token for Azure Resource Manager APIs.

    Returns:
        str: Bearer token string used for Azure REST API requests.

    Raises:
        Exception: If authentication fails.
    """
    credential = DefaultAzureCredential()
    token = credential.get_token(settings.AZURE_MANAGEMENT_SCOPE)
    return token.token


def build_scope(
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


def build_storage_resource_id(
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

    scope = build_scope(
        billing_account_id,
        billing_profile_id,
    )

    storage_resource_id = build_storage_resource_id(
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