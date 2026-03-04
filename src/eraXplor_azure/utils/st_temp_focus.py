"""
Create:
1. Azure Storage Account
2. Blob Container
3. Virtual Folder inside container

Authentication: DefaultAzureCredential
"""

import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError


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

    # ---------------------------------------------------------
    # 1️⃣ Create Storage Account
    # ---------------------------------------------------------
    storage_client = StorageManagementClient(credential, subscription_id)

    print(f"Creating storage account '{storage_account_name}'...")

    poller = storage_client.storage_accounts.begin_create(
        resource_group_name,
        storage_account_name,
        StorageAccountCreateParameters(
            sku=Sku(name="Standard_LRS"),
            kind="StorageV2",
            location=location,
        ),
    )

    account_result = poller.result()
    print("Storage account created successfully.")

    # ---------------------------------------------------------
    # 2️⃣ Get Storage Account Key
    # ---------------------------------------------------------
    keys = storage_client.storage_accounts.list_keys(
        resource_group_name,
        storage_account_name,
    )

    account_key = keys.keys[0].value

    account_url = f"https://{storage_account_name}.blob.core.windows.net"

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
    # Azure Blob does not have real folders.
    # We simulate it by creating an empty blob ending with "/"
    folder_blob_name = f"{folder_name}/"

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=folder_blob_name,
    )

    blob_client.upload_blob(b"", overwrite=True)

    print(f"Folder '{folder_name}/' created successfully.")


if __name__ == "__main__":

    create_storage_account_container_folder(
        subscription_id="YOUR_SUBSCRIPTION_ID",
        resource_group_name="YOUR_RESOURCE_GROUP",
        location="eastus",
        storage_account_name="uniquestorageacct12345",  # must be globally unique
        container_name="my-container",
        folder_name="my-folder",
    )