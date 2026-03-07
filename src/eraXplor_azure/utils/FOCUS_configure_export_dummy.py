import requests
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta, UTC
import json


def create_focus_export(
    billingAccountId: str,
    billingProfileId: str,
    subscription_id: str,
    resource_group_name: str,
    storage_account_name: str,
    container_name: str,
    folder_name: str,
    export_name: str = "focus-cost-export",
):

    start = (datetime.now(UTC) + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    end = "2030-01-01T00:00:00Z"

    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default").token

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    scope = (
        f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}"
        f"/billingProfiles/{billingProfileId}"
    )

    storage_resource_id = (
        f"/subscriptions/{subscription_id}"
        f"/resourceGroups/{resource_group_name}"
        f"/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"
    )

    body = {
        "location": "global",
        "identity": {"type": "SystemAssigned"},
        "properties": {
            "definition": {
                "type": "FocusCost",
                "timeframe": "MonthToDate",
                "dataset": {
                    "granularity": "Daily",
                    "configuration": {"dataVersion": "1.0"},
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
                "recurrencePeriod": {"from": start, "to": end},
            },
        },
    }

    url = (
        f"https://management.azure.com{scope}"
        f"/providers/Microsoft.CostManagement/exports/{export_name}"
        f"?api-version=2023-07-01-preview"
    )

    print("\nScope:", scope)
    print("\nCreating export...")
    print(json.dumps(body, indent=2))

    response = requests.put(url, headers=headers, json=body)

    print("\nStatus:", response.status_code)
    print(response.text)


if __name__ == "__main__":

    billingAccountId = "ca9bd292-e90d-5f53-0554-6dffa0ce3a9c:c1ca22c2-98ed-43c5-91bc-feba5db2d6ed_2019-05-31"
    billingProfileId = "ZPQJ-IN76-BG7-PGB"

    subscription_id = "856880af-e2ac-41b2-b5fb-e7ebfe4d97bc"

    resource_group_name = "focusstorage-rg-02"
    storage_account_name = "focusstorageacct123456"

    container_name = "focus-export-container"
    folder_name = "focus-export-folder"

    create_focus_export(
        billingAccountId,
        billingProfileId,
        subscription_id,
        resource_group_name,
        storage_account_name,
        container_name,
        folder_name,
    )
################################################################



# from azure.identity import ClientSecretCredential
# from azure.mgmt.costmanagement import CostManagementClient

# tenant_id = "TENANT_ID"
# client_id = "CLIENT_ID"
# client_secret = "CLIENT_SECRET"
# subscription_id = "SUBSCRIPTION_ID"

# credential = ClientSecretCredential(
#     tenant_id=tenant_id,
#     client_id=client_id,
#     client_secret=client_secret
# )

# client = CostManagementClient(credential)

# scope = f"/subscriptions/{subscription_id}"

# export_name = "focus-cost-export"

# export_definition = {
#     "properties": {
#         "definition": {
#             "type": "FocusCost",
#             "timeframe": "MonthToDate",
#             "dataset": {
#                 "granularity": "Daily"
#             }
#         },
#         "deliveryInfo": {
#             "destination": {
#                 "resourceId": f"/subscriptions/{subscription_id}/resourceGroups/rg-finops/providers/Microsoft.Storage/storageAccounts/mystorage",
#                 "container": "costexports",
#                 "rootFolderPath": "focus"
#             }
#         },
#         "format": "Parquet",
#         "partitionData": True,
#         "schedule": {
#             "status": "Active",
#             "recurrence": "Daily"
#         }
#     }
# }

# result = client.exports.create_or_update(
#     scope=scope,
#     export_name=export_name,
#     parameters=export_definition
# )

# print(result)