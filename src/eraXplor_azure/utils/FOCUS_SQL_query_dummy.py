import duckdb
import fsspec
from azure.identity import DefaultAzureCredential
import tempfile
import os
import shutil
import warnings
import pandas as pd
from tabulate import tabulate  # pip install tabulate if needed

# -----------------------------
# Configuration
# -----------------------------
account = "focusstorageacct123456"
container = "focus-export-container"
base_path = "focus-export-folder/focus-cost-export"

# -----------------------------
# Suppress exit-time warnings from fsspec/adlfs
# -----------------------------
warnings.filterwarnings("ignore", category=RuntimeWarning)

# -----------------------------
# Azure AD Authentication
# -----------------------------
credential = DefaultAzureCredential()
fs = fsspec.filesystem(
    "az",
    account_name=account,
    credential=credential,
    asynchronous=False
)

# -----------------------------
# Recursively list all parquet files
# -----------------------------
files = fs.glob(f"{container}/{base_path}/**/*.parquet")
if not files:
    raise RuntimeError(f"No parquet files found in {container}/{base_path}")

print(f"Found {len(files)} parquet files.")

# -----------------------------
# Download all parquet files locally
# -----------------------------
tmp_dir = tempfile.mkdtemp()
local_files = []
for f in files:
    local_path = os.path.join(tmp_dir, os.path.basename(f))
    fs.get(f, local_path)
    local_files.append(local_path)

print(f"Downloaded {len(local_files)} files to {tmp_dir}")

# -----------------------------
# Connect to DuckDB
# -----------------------------
con = duckdb.connect()

# -----------------------------
# Pandas display options for readability
# -----------------------------
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.width", 0)  # auto-wrap wide tables

# -----------------------------
# Read all parquet files into DuckDB table
# -----------------------------
df = con.execute(f"SELECT * FROM read_parquet({local_files})").fetchdf()

# -----------------------------
# Print table in human-readable format
# -----------------------------
print(tabulate(df.head(), headers='keys', tablefmt='grid', showindex=False))

# -----------------------------
# Clean up filesystem reference to avoid exit-time TypeError
# -----------------------------
if hasattr(fs, "close"):
    fs.close()
del fs

# -----------------------------
# Optional: remove temporary files after processing
# -----------------------------
# shutil.rmtree(tmp_dir)