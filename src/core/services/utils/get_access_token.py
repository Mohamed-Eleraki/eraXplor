"""
Shared Azure authentication utility functions.

This module provides reusable authentication helpers for Azure services.
"""

from azure.identity import DefaultAzureCredential

from api.config import settings


def get_access_token() -> str:
    """
    Retrieve an Azure access token using DefaultAzureCredential.

    This function authenticates against Azure Active Directory and
    requests a token for Azure Resource Manager APIs.

    Returns:
        str: Azure bearer token for ARM API requests.

    Raises:
        RuntimeError: If Azure authentication fails.
    """
    try:
        credential = DefaultAzureCredential()

        token = credential.get_token(
            settings.AZURE_MANAGEMENT_SCOPE
        )

        return token.token

    except Exception as exc:
        raise RuntimeError(
            "Failed to retrieve Azure access token."
        ) from exc