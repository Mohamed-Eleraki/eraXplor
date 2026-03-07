import duckdb
import fsspec

# Connect to Azure Storage
fs = fsspec.filesystem(
    "abfs",
    account_name="focusstorageacct123456",
    credential="<YOUR_CREDENTIAL>"  # can be DefaultAzureCredential
)

# Query all Parquet files in the folder
query = """
SELECT
    usageDate,
    subscriptionId,
    resourceId,
    meterCategory,
    costUSD
FROM 'focus-export-folder/*.parquet'
"""

# Execute query using DuckDB
con = duckdb.connect()
df = con.execute(query, filesystem=fs).fetchdf()

print(df.head())