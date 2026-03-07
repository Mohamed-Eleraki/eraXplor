"""
Create:
1. Azure Resource Group
2. Azure Storage Account
3. Blob Container
4. Virtual Folder inside container

Authentication: DefaultAzureCredential
"""

import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError


def create_resource_group(subscription_id: str, resource_group_name: str, location: str):
    """
    Creates a resource group if it does not exist.
    """

    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)

    print(f"Creating resource group '{resource_group_name}'...")

    resource_client.resource_groups.create_or_update(
        resource_group_name,
        {"location": location},
    )

    print(f"Resource group '{resource_group_name}' created or already exists.")


def create_storage_account_container_folder(
    subscription_id: str,
    resource_group_name: str,
    location: str,
    storage_account_name: str,
    container_name: str,
    folder_name: str,
):
    """
    Creates storage account, container, and folder (virtual directory).
    """

    credential = DefaultAzureCredential()
    account_name = storage_account_name.lower()

    # ---------------------------------------------------------
    # 1️⃣ Create Storage Account
    # ---------------------------------------------------------
    storage_client = StorageManagementClient(credential, subscription_id)

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

    # ---------------------------------------------------------
    # 2️⃣ Get Storage Account Key
    # ---------------------------------------------------------
    keys = storage_client.storage_accounts.list_keys(
        resource_group_name,
        account_name,
    )

    account_key = keys.keys[0].value
    account_url = f"https://{account_name}.blob.core.windows.net"

    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=account_key,
    )

    # ---------------------------------------------------------
    # 3️⃣ Create Container
    # ---------------------------------------------------------
    try:
        blob_service_client.create_container(container_name)
        print(f"Container '{container_name}' created.")
    except ResourceExistsError:
        print(f"Container '{container_name}' already exists.")

    # ---------------------------------------------------------
    # 4️⃣ Create Folder (Virtual Directory)
    # ---------------------------------------------------------
    folder_blob_name = f"{folder_name}/"

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=folder_blob_name,
    )

    blob_client.upload_blob(b"", overwrite=True)

    print(f"Folder '{folder_name}/' created successfully.")


if __name__ == "__main__":

    subscription_id = "856880af-e2ac-41b2-b5fb-e7ebfe4d97bc"
    resource_group_name = "focusstorage-rg-02"
    location = "westeurope"

    storage_account_name = "focusstorageacct123456"
    container_name = "focus-export-container"
    folder_name = "focus-export-folder"

    # 1️⃣ Create Resource Group first
    create_resource_group(
        subscription_id,
        resource_group_name,
        location,
    )

    # 2️⃣ Create Storage + Container + Folder
    create_storage_account_container_folder(
        subscription_id,
        resource_group_name,
        location,
        storage_account_name,
        container_name,
        folder_name,
    )