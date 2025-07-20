import datetime
import threading
from typing import Dict, List, TypedDict
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient, models
from rich.live import Live
from rich.spinner import Spinner

class _CostRecord(TypedDict):
    """Class type annotation tool dettermining the List Schema.
    Type definition for a single cost record.
    """
    TIME_PERIOD: Dict[str, str]
    COST: str

def cost_export(
    subscription_id: str, 
    start_date: str, 
    end_date: str,
    granularity: str = 'Daily',
) -> List[_CostRecord]:
    
    credential = DefaultAzureCredential()
    cm_client = CostManagementClient(credential)
    
    start_date = datetime.datetime.strptime(start_date, "%Y,%m,%d")
    end_date = datetime.datetime.strptime(end_date, "%Y,%m,%d")
    scope = f"/subscriptions/{subscription_id}"
    # scope = f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
    # scope = f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}"
    # scope = f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/departments/{departmentId}"
    # scope = f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/enrollmentAccounts/{enrollmentAccountId}"
    # scope = f"/providers/Microsoft.Management/managementGroups/{managementGroupId}"
    # scope = f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/billingProfiles/{billingProfileId}"
    # scope = f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/billingProfiles/{billingProfileId}/invoiceSections/{invoiceSectionId}"
    # scope = f"/providers/Microsoft.Billing/billingAccounts/{billingAccountId}/customers/{customerId}"
    
    
    
    cm_client_query_results = []
    with Live(Spinner
              ("bouncingBar", text=f"Fetching Azure costs of subscriptions:{subscription_id}...\n\n"),
                refresh_per_second=10):
        def _sub_cost_export():
             
            try:
                cm_client_query = cm_client.query.usage(
                    scope=scope,
                    parameters=models.QueryDefinition(
                        type='Usage',
                        timeframe='Custom',
                        time_period=models.QueryTimePeriod(
                            from_property=start_date,
                            to=end_date,
                        ),
                        dataset=models.QueryDataset(
                            granularity=granularity,
                            aggregation={
                                'totalcost': models.QueryAggregation(name='PreTaxCost', function='Sum')
                            }
                        )
                    )
                )
                cm_client_query_rows = cm_client_query.rows
                for row in cm_client_query_rows:
                    time_period = row[1]
                    cost = row[0]
                    currency = row[2]
                    
                    cm_client_query_results.append(
                        {
                            "TIME_PERIOD": time_period,
                            "COST": f"{cost:.2f} {currency}",
                        }
                    )
                    
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)}

        # progress.update(task, advance=1)
        thread = threading.Thread(target=_sub_cost_export)
        thread.start()
        thread.join()
    return cm_client_query_results

# cm_client_query_results = cost_export("856880af-e2ac-41b2-b5fb-e7ebfe4d97bc", "2025,1,1", "2025,4,30", "monthly")
# print(cm_client_query_results)