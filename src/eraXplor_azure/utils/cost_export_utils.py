"""Module for exporting Azure cost data using the Azure Cost Management API."""

import json
import datetime
import threading
from typing import Dict, List, TypedDict, Any
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient, models
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod
from azure.mgmt.resource import SubscriptionClient
from rich.live import Live
from rich.spinner import Spinner

class _CostRecord(TypedDict):
    """Class type annotation tool dettermining the List Schema.
    Type definition for a single cost record.
    """
    TIME_PERIOD: Dict[str, str]
    COST: str

def cost_export(
    subscription_id: str | None = None, 
    subscriptions_list_detailed: List[dict[str, Any]] = None, 
    start_date: str = None, 
    end_date: str = None,
    granularity: str = 'Monthly',
) -> List[_CostRecord]:
    """
        Retrieve Azure cost data for a given subscription and time range.

        Executes a cost management query using the Azure Cost Management API to 
        extract cost data for a specific subscription, aggregated by the 
        selected granularity (Daily or Monthly).

        Args:
            subscription_id (str): 
                [REQUIRED] Azure subscription ID to query cost data for.
            
            start_date (str): 
                [REQUIRED] Start date of the report period (inclusive).
                Format: "YYYY,MM,DD"
                Default: 3 Months ago from today.
            
            end_date (str): 
                [REQUIRED] End date of the report period (inclusive).
                Format: "YYYY,MM,DD"
                Default: Today date.
            
            granularity (str): 
                [OPTIONAL] Level of time granularity for aggregation.
                Default: "Monthly"
                Valid values:
                    - "Daily": Daily cost records
                    - "Monthly": Monthly aggregated cost records

        Returns:
            List[_CostRecord]: 
                A list of structured cost records, where each record contains:
                    - TIME_PERIOD (Dict[str, str]): Date or date range for the record.
                    - COST (str): Formatted string representing the total cost and currency (e.g., "123.45 USD").

        Raises:
            Exception: For any API errors or authentication failures.

        Example:
            >>> cost_export(
            ...     subscription_id="SUB_ID",
            ...     start_date="2025,01,01",
            ...     end_date="2025,04,30",
            ...     granularity="Monthly"
            ... )
            [{'TIME_PERIOD': {'Start': '2025-01-01', 'End': '2025-01-31'}, 'COST': '456.78 USD'}, ...]

        Notes:
            - Ensure that the environment is properly authenticated with Azure using `DefaultAzureCredential`.
            - Date strings must follow the exact "YYYY,MM,DD" format to avoid parsing errors.
            - Depending on the size of the date range and granularity, response time may vary.
        """
    
    credential = DefaultAzureCredential()
    cm_client = CostManagementClient(credential)
    cm_client_query_results = []
    
    if subscription_id is not None:
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
        
        with Live(Spinner
                ("bouncingBar", text=f"Fetching Azure costs of subscriptions: {subscription_id}...\n\n"),
                    refresh_per_second=10):
            def _sub_cost_export():
                """Internal function to handle the cost export query."""
                
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
                                "SUBSCRIPTION_ID": subscription_id,
                                "DISPLAY_NAME": "NONE",
                                "COST": f"{cost:.2f} {currency}",
                                "TAGS": "None"
                            }
                        )
                    print(json.dumps(cm_client_query_results, indent=4, default=str), end="\n\n\n")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return {"error": str(e)}

            # progress.update(task, advance=1)
            _thread = threading.Thread(target=_sub_cost_export)
            _thread.start()
            _thread.join()
            
    if subscription_id is None:
        start_date = datetime.datetime.strptime(start_date, "%Y,%m,%d")
        end_date = datetime.datetime.strptime(end_date, "%Y,%m,%d")
        
        for sub in subscriptions_list_detailed:
            subscription_id = sub['Subscription_ID']
            subscription_name = sub['Display_Name']
            subscription_tags = sub.get('Tags', {})
            scope = f"/subscriptions/{subscription_id}"
            
            with Live(Spinner
                    ("bouncingBar", text=f"Fetching Azure costs of subscriptions: {subscription_name}({subscription_id})...\n\n"),
                        refresh_per_second=10):
                def _sub_cost_export():
                    """Internal function to handle the cost export query."""
                    
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
                                    "SUBSCRIPTION_ID": subscription_id,
                                    "DISPLAY_NAME": subscription_name,
                                    "COST": f"{cost:.2f} {currency}",
                                    "TAGS": subscription_tags if subscription_tags else "None"
                                }
                            )
                            # print(json.dumps(cm_client_query_results, indent=4, default=str), end="\n\n\n")
                        # Combine results of for loop and print
                        print(json.dumps([
                            {
                                "TIME_PERIOD": row[1],
                                "SUBSCRIPTION_ID": subscription_id,
                                "DISPLAY_NAME": subscription_name,
                                "COST": f"{row[0]:.2f} {row[2]}",
                                "TAGS": subscription_tags if subscription_tags else "None",
                            } for row in cm_client_query_rows
                        ], indent=4, default=str), end="\n\n\n")

                    except Exception as e:
                        print(f"An error occurred: {e}")
                        return {"error": str(e)}

                # progress.update(task, advance=1)
                _thread = threading.Thread(target=_sub_cost_export)
                _thread.start()
                _thread.join()
            
    return cm_client_query_results

# cm_client_query_results = cost_export("856880af-e2ac-41b2-b5fb-e7ebfe4d97bc", "2025,1,1", "2025,4,30", "monthly")
# print(cm_client_query_results)

def subs_cost_export():
    """Function to retrieve Azure subscription details"""
    _credential = DefaultAzureCredential()
    _subscription_client = SubscriptionClient(_credential)
    _subscriptions = list(_subscription_client.subscriptions.list())
    
    subscriptions_list_detailed = []
    subscriptions_with_tags_list = []
    
    for sub in _subscriptions:
        subscriptions_list_detailed.append(
            {
                "Subscription_ID": sub.subscription_id,
                "Display_Name": sub.display_name,
                "Tenant_ID": sub.tenant_id,
                "Tags": sub.tags,
            }
        )
        subscriptions_with_tags_list.append(
            {
                "Subscription_ID": sub.subscription_id,
                "Display_Name": sub.display_name,
                "Tags": sub.tags,
            }
        )
    return subscriptions_list_detailed, subscriptions_with_tags_list

# import json
# subscriptions_list_detailed, subscriptions_with_tags_list = subs_cost_export()
# cm_client_query_results = cost_export(subscription_id="856880af-e2ac-41b2-b5fb-e7ebfe4d97bc", subscriptions_list_detailed=subscriptions_list_detailed, start_date="2025,5,1", end_date="2025,6,30", granularity="Monthly")
# # print(json.dumps(cm_client_query_results, indent=4, default=str))

