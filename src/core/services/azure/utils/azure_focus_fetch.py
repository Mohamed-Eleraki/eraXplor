"""
Module for fetching Parquet files from Azure Blob Storage for FOCUS data export.
This module provides a function to download Parquet files from a specified folder
(virtual directory) within an Azure Blob Storage container.

ARGS:
- storage_account_name: Name of the Storage Account
- container_name: Name of the Blob Container
- folder_name: Name of the Folder (Virtual Directory) within the Blob Container

Dependencies:
- azure-identity
- azure-storage-blob
"""

import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient


def download_parquet_files(
    storage_account_name: str,
    container_name: str,
    folder_name: str,
) -> list:
    """
    Download Parquet files from Azure Blob Storage.

    Args:
        storage_account_name: Name of the Storage Account.
        container_name: Name of the Blob Container.
        folder_name: Name of the virtual directory within the Blob Container.

    Returns:
        List of paths to the downloaded Parquet files.
    """

    local_download_path = "./downloaded_parquet_files"
    os.makedirs(local_download_path, exist_ok=True)

    credential = DefaultAzureCredential()

    container_client = ContainerClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        container_name=container_name,
        credential=credential,
    )

    print(
        f"Listing blobs in container '{container_name}' "
        f"under folder '{folder_name}'..."
    )

    blob_list = container_client.list_blobs(
        name_starts_with=f"{folder_name}/"
    )

    downloaded_files = []

    for blob in blob_list:
        
        print(f"Found blob: {blob.name}")
        blob_name = blob.name

        # Skip the virtual folder blob and non-Parquet files.
        if blob_name.endswith("/") or not blob_name.lower().endswith(".parquet"):
            continue

        file_name = os.path.basename(blob_name)

        download_file_path = os.path.join(
            local_download_path,
            file_name,
        )

        with open(download_file_path, "wb") as file:
            file.write(
                container_client.download_blob(blob_name).readall()
            )

        downloaded_files.append(download_file_path)
        print(f"Downloaded: {download_file_path}")

    return downloaded_files