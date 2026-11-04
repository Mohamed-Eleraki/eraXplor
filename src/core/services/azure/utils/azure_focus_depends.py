"""
Module for installing dependencies required for Azure FOCUS data export.

This module provides functions to create necessary Azure resources for FOCUS data export, including:
- Resource Group
- Storage Account
- Blob Container
- Folder (Virtual Directory) within the Blob Container  

ARGS:
- subscription_id: Azure Subscription ID
- resource_group_name: Name of the Resource Group to create
- location: Azure region for the resources
- storage_account_name: Name of the Storage Account to create
- container_name: Name of the Blob Container to create
- folder_name: Name of the Folder (Virtual Directory) to create within the Blob Container

Dependencies:
- azure-identity
- azure-mgmt-storage
- azure-mgmt-resource
- azure-storage-blob
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku
try:
    from azure.mgmt.resource import ResourceManagementClient
except ImportError:
    from azure.mgmt.resource.resources import ResourceManagementClient
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

def create_resource_group(
        subscription_id: str,
        resource_group_name: str = "focus-data-export-rg",
        location: str = "eastus",
        ) -> None:
    """
    Creates a resource group if it does not exist.
    """

    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    
    resource_client.resource_groups.create_or_update(
        resource_group_name,
        {"location": location},
    )
    print(f"Resource group '{resource_group_name}' created or already exists.")


def create_storage_account_container_folder(
    subscription_id: str,
    resource_group_name: str = "focus-data-export-rg",
    location: str = "eastus",
    storage_account_name: str = "focusdataexportstorage",
    container_name: str = "focus-data",
    folder_name: str = "focus-exports",
    ) -> None:
    """
    Creates storage account, container, and folder (virtual directory).
    """

    credential = DefaultAzureCredential()
    account_name = storage_account_name.lower()
    storage_client = StorageManagementClient(credential, subscription_id)

    # Create Storage Account
    print(f"Creating storage account '{account_name}'...")
    poller = storage_client.storage_accounts.begin_create(
        resource_group_name,
        account_name,
        StorageAccountCreateParameters(
            sku=Sku(name="Standard_LRS"),
            kind="StorageV2",
            location=location,
        ),
    )
    poller.result()
    print("Storage account created successfully.")

    # Get Storage Account Key
    keys = storage_client.storage_accounts.list_keys(
        resource_group_name,
        account_name,
    )

    keys_dict = keys.as_dict()

    account_key = keys_dict["keys"][0]["value"]
    account_url = f"https://{account_name}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=account_key,
    )

    # Create Container
    try:
        blob_service_client.create_container(container_name)
        print(f"Container '{container_name}' created.")
    except ResourceExistsError:
        print(f"Container '{container_name}' already exists.")

    # Create Folder (Virtual Directory)
    folder_blob_name = f"{folder_name}/"
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=folder_blob_name,
    )
    blob_client.upload_blob(b"", overwrite=True)
    print(f"Folder '{folder_name}/' created successfully.")
