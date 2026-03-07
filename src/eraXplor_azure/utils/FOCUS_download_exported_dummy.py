# FOCUS_parquet_to_csv.py
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
import pyarrow.parquet as pq
import pandas as pd

# -----------------------------
# CONFIGURATION
# -----------------------------
storage_account_name = "focusstorageacct123456"
container_name = "focus-export-container"
folder_name = "focus-export-folder"
local_download_path = "./focus_parquet_files"  # temporary download folder
output_csv = "focus_cost_report.csv"

os.makedirs(local_download_path, exist_ok=True)

# -----------------------------
# DOWNLOAD PARQUET FILES FROM AZURE STORAGE
# -----------------------------
def download_parquet_files():
    credential = DefaultAzureCredential()
    container_client = ContainerClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        container_name=container_name,
        credential=credential,
    )

    print(f"Listing blobs in container '{container_name}' under folder '{folder_name}'...")
    blob_list = container_client.list_blobs(name_starts_with=f"{folder_name}/")

    downloaded_files = []
    for blob in blob_list:
        blob_name = blob.name
        download_file_path = os.path.join(local_download_path, os.path.basename(blob_name))
        with open(download_file_path, "wb") as f:
            f.write(container_client.download_blob(blob_name).readall())
        downloaded_files.append(download_file_path)
        print(f"Downloaded: {download_file_path}")

    return downloaded_files

# -----------------------------
# COMBINE PARQUET FILES INTO CSV
# -----------------------------
def combine_parquet_to_csv(parquet_files):
    all_dfs = []
    for file_path in parquet_files:
        table = pq.read_table(file_path)
        df = table.to_pandas()
        all_dfs.append(df)

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df.to_csv(output_csv, index=False)
        print(f"\n✅ Combined CSV saved: {output_csv}")
    else:
        print("\n⚠️ No Parquet files found to combine.")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    parquet_files = download_parquet_files()
    combine_parquet_to_csv(parquet_files)