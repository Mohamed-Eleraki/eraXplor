"""
Module for exporting Azure cost data using the Azure Cost Management API.

This module provides functionality to query and retrieve Azure cost and usage data
using the Azure Cost Management API. It supports multiple grouping dimensions
including subscription, ServiceName, and ResourceGroupName, with both daily and
monthly granularity options.

The module includes:
    - cost_export: Main function to fetch cost data across all subscriptions
    - list_subs: Retrieves details of all accessible Azure subscriptions
    - _subs_cost_export: Internal function for subscription-level cost export
    - _cost_export_subfunc: Internal function for dimension-based cost export

Dependencies:
    - azure-identity: For DefaultAzureCredential authentication
    - azure-mgmt-costmanagement: For Cost Management API access
    - azure-mgmt-resource: For Subscription Client access
    - rich: For live progress display

Example:
    >>> from eraXplor_azure.utils.cost_export_utils import cost_export, list_subs
    >>> subscriptions = list_subs()
    >>> cost_data = cost_export(
    ...     group_by='subscription',
    ...     subscriptions_list_detailed=subscriptions,
    ...     start_date='2025,01,01',
    ...     end_date='2025,01,31',
    ...     granularity='Monthly'
    ... )
"""

import json
import datetime
import threading
from typing import List, TypedDict, Any
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient, models
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod  # Pylint: disable=unused-import
from rich.live import Live
from rich.spinner import Spinner

try:
    from azure.mgmt.resource import SubscriptionClient
    HAS_SUBSCRIPTION_CLIENT = True
except ImportError:
    HAS_SUBSCRIPTION_CLIENT = False

class _CostRecord(TypedDict):
    """
    Type definition for a single cost record returned by cost_export.

    This TypedDict defines the schema for cost records, providing type hints
    for the dictionary structure returned by the cost_export function.

    Attributes:
        TIME_PERIOD: Date or date range for the cost record.
                     For monthly granularity: {'Start': 'YYYY-MM-DD', 'End': 'YYYY-MM-DD'}
                     For daily granularity: date string in 'YYYY-MM-DD' format
        GROUP_BY: The grouping dimension used (e.g. 'SUBSCRIPTION_ID', 'ServiceName')
        SUBSCRIPTION_ID: The Azure subscription ID associated with the cost
        DISPLAY_NAME: The subscription display name
        PreTaxCost: Cost amount formatted as string with currency (e.g. "123.45 USD")
        TAGS: Dictionary of subscription tags or "None" if no tags exist
    """
    TIME_PERIOD: Any
    GROUP_BY: str
    SUBSCRIPTION_ID: str
    DISPLAY_NAME: str
    PreTaxCost: str
    TAGS: dict[str, Any] | str

def cost_export(
    group_by: str = 'subscription',
    subscriptions_list_detailed: List[dict[str, Any]] = None,
    start_date: str = None,
    end_date: str = None,
    granularity: str = 'Monthly',
) -> List[_CostRecord]:
    """
    Retrieve Azure cost data for all subscriptions over a specified time range.

    Executes cost management queries using the Azure Cost Management API to extract
    cost data for all accessible subscriptions, aggregated by the selected dimension
    and granularity (Daily or Monthly).

    This is the main entry point for fetching cost data. The function delegates to
    internal helper functions based on the group_by parameter:
        - 'subscription': Uses _subs_cost_export for per-subscription breakdown
        - 'ServiceName' or 'ResourceGroupName': Uses _cost_export_subfunc

    Args:
        group_by (str, optional):
            Dimension to group costs by. Valid values:
            - 'subscription' (default): Group by Azure subscription
            - 'ServiceName': Group by Azure service name
            - 'ResourceGroupName': Group by resource group

        subscriptions_list_detailed (List[dict[str, Any]], optional):
            List of subscription dictionaries as returned by list_subs().
            Each dictionary should contain 'Subscription_ID', 'Display_Name',
            and 'Tags'. If None, the function will attempt to retrieve
            subscriptions automatically.

        start_date (str, optional):
            Start date of the report period (inclusive).
            Format: "YYYY,MM,DD"
            Default: 3 months ago from today.

        end_date (str, optional):
            End date of the report period (inclusive).
            Format: "YYYY,MM,DD"
            Default: Today's date.

        granularity (str, optional):
            Level of time granularity for aggregation. Valid values:
            - 'Monthly' (default): Monthly aggregated cost records
            - 'Daily': Daily cost records

    Returns:
        List[_CostRecord]:
            A list of structured cost records, where each record contains:
            - TIME_PERIOD: Date or date range (dict with 'Start'/'End' keys for monthly,
              string for daily)
            - GROUP_BY: The grouping dimension used
            - SUBSCRIPTION_ID: Azure subscription ID
            - DISPLAY_NAME: Subscription display name
            - PreTaxCost: Formatted cost string with currency (e.g. "123.45 USD")
            - TAGS: Dictionary of subscription tags or "None"

    Raises:
        azure.core.exceptions.AzureError: For Azure API errors.
        Exception: For any authentication failures or network issues.

    Example:
        >>> from eraXplor_azure.utils.cost_export_utils import cost_export, list_subs
        >>> subs = list_subs()
        >>> costs = cost_export(
        ...     group_by='subscription',
        ...     subscriptions_list_detailed=subs,
        ...     start_date='2025,01,01',
        ...     end_date='2025,01,31',
        ...     granularity='Monthly'
        ... )
        >>> for record in costs:
        ...     print(f"{record['DISPLAY_NAME']}: {record['PreTaxCost']}")

    Notes:
        - Ensure that the environment is properly authenticated with Azure using
          `DefaultAzureCredential`.
        - Date strings must follow the exact "YYYY,MM,DD" format to avoid parsing errors.
        - Depending on the size of the date range and granularity, response time may vary.
        - The function displays progress using rich.live for real-time feedback.
    """
    
    credential = DefaultAzureCredential()
    cm_client = CostManagementClient(credential)
    cm_client_query_results = []

    if group_by == 'subscription':
        _subs_cost_export(
            group_by=group_by,
            subscriptions_list_detailed=subscriptions_list_detailed,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
            cm_client=cm_client,
            cm_client_query_results=cm_client_query_results,
        )
        return cm_client_query_results


    if group_by == 'ServiceName':
        _cost_export_subfunc(
            group_by=group_by,
            subscriptions_list_detailed=subscriptions_list_detailed,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
            cm_client=cm_client,
            cm_client_query_results=cm_client_query_results,
        )
        return cm_client_query_results    
    
    if group_by == 'ResourceGroupName':
        _cost_export_subfunc(
            group_by=group_by,
            subscriptions_list_detailed=subscriptions_list_detailed,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
            cm_client=cm_client,
            cm_client_query_results=cm_client_query_results,
        )
        return cm_client_query_results   



def list_subs():
    """
    Retrieve details of all Azure subscriptions accessible by the authenticated principal.

    Uses the Azure SubscriptionClient if available, otherwise falls back to the ARM REST API.
    Returns detailed information including subscription ID, display name, tenant ID, and tags.

    Returns:
        List[dict[str, Any]]:
            A list of subscription dictionaries, where each dictionary contains:
            - 'Subscription_ID' (str): The unique Azure subscription ID
            - 'Display_Name' (str): The human-readable subscription name
            - 'Tenant_ID' (str): The Azure tenant ID associated with the subscription
            - 'Tags' (dict or None): Dictionary of subscription tags if any exist

    Raises:
        azure.core.exceptions.AzureError: For Azure API errors.
        Exception: For authentication failures.

    Example:
        >>> from eraXplor_azure.utils.cost_export_utils import list_subs
        >>> subscriptions = list_subs()
        >>> for sub in subscriptions:
        ...     print(f"{sub['Display_Name']}: {sub['Subscription_ID']}")

    Note:
        - Requires appropriate Azure RBAC permissions to list subscriptions.
        - The authenticated principal must have Reader role or equivalent
          on the subscriptions to be listed.
        - Tags are optional and may be None for subscriptions without tags.
    """
    _credential = DefaultAzureCredential()
    subscriptions_list_detailed = []
    
    # Try using SubscriptionClient if available
    if HAS_SUBSCRIPTION_CLIENT:
        try:
            _subscription_client = SubscriptionClient(_credential)
            _subscriptions = list(_subscription_client.subscriptions.list())
            
            for sub in _subscriptions:
                subscriptions_list_detailed.append(
                    {
                        "Subscription_ID": sub.subscription_id,
                        "Display_Name": sub.display_name,
                        "Tenant_ID": sub.tenant_id,
                        "Tags": sub.tags,
                    }
                )
            return subscriptions_list_detailed
        except Exception:
            pass  # Fall through to REST API fallback
    
    # Fallback to ARM REST API
    from core.services.utils.get_access_token import get_access_token
    import requests
    
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    url = "https://management.azure.com/subscriptions?api-version=2020-01-01"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    for sub in data.get("value", []):
        subscriptions_list_detailed.append(
            {
                "Subscription_ID": sub.get("subscriptionId"),
                "Display_Name": sub.get("displayName"),
                "Tenant_ID": sub.get("tenantId"),
                "Tags": sub.get("tags"),
            }
        )
    
    return subscriptions_list_detailed


def _subs_cost_export(
    group_by: str = 'subscription',  # Pylint: disable=unused-argument
    subscriptions_list_detailed: List[dict[str, Any]] = None,
    start_date: str = None,
    end_date: str = None,
    granularity: str = 'Monthly',
    cm_client: CostManagementClient = None,
    cm_client_query_results = None,
):
    """
    Internal function to fetch Azure costs grouped by subscription.

    Executes cost management queries for each subscription in the provided list,
    aggregating costs by subscription ID. This is an internal helper function
    called by cost_export() when group_by='subscription'.

    Args:
        group_by (str, optional):
            Grouping dimension. Currently only 'subscription' is supported.
            Defaults to 'subscription'.

        subscriptions_list_detailed (List[dict[str, Any]]):
            List of subscription dictionaries as returned by list_subs().
            Each dictionary must contain 'Subscription_ID', 'Display_Name',
            and optionally 'Tags'.

        start_date (str):
            Start date in "YYYY,MM,DD" format. Inclusive.

        end_date (str):
            End date in "YYYY,MM,DD" format. Inclusive.

        granularity (str, optional):
            Time granularity for cost aggregation. Valid values:
            - 'Monthly' (default): Monthly aggregated costs
            - 'Daily': Daily cost records

        cm_client (CostManagementClient):
            Pre-initialized Azure CostManagementClient instance.

        cm_client_query_results (list):
            List to append cost records to. Modified in-place.

    Returns:
        List[dict]: Updated cost records list with subscription-level data.

    Note:
        This is an internal function and should not be called directly.
        It uses threading for each subscription query and displays
        progress using rich.live.
    """
    start_date = datetime.datetime.strptime(start_date, "%Y,%m,%d")
    end_date = datetime.datetime.strptime(end_date, "%Y,%m,%d")
    subscription_id = ""
    subscription_name = ""
    subscription_tags = ""

    for sub in subscriptions_list_detailed:
        subscription_id = sub['Subscription_ID']
        subscription_name = sub['Display_Name']
        subscription_tags = sub.get('Tags', {})
        scope = f"/subscriptions/{subscription_id}"
        
        with Live(Spinner
                ("bouncingBar", text=f"Fetching Azure costs of subscriptions: "
                 f"{subscription_name}({subscription_id})...\n\n"),
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
                                    'totalcost': models.QueryAggregation(
                                        name='PreTaxCost',
                                        function='Sum')
                                }
                            )
                        )
                    )
                    cm_client_query_rows = cm_client_query.rows
                    for row in cm_client_query_rows:
                        time_period = row[1]
                        PreTaxCost = row[0]
                        currency = row[2]
                        
                        cm_client_query_results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "GROUP_BY": "SUBSCRIPTION_ID",
                                "SUBSCRIPTION_ID": subscription_id,
                                "DISPLAY_NAME": subscription_name,
                                "PreTaxCost": f"{PreTaxCost:.2f} {currency}",
                                "TAGS": subscription_tags if subscription_tags else "None"
                            }
                        )

                    # Combine results of for loop and print
                    print(json.dumps([
                        {
                            "TIME_PERIOD": row[1],
                            "GROUP_BY": "SUBSCRIPTION_ID",
                            "SUBSCRIPTION_ID": subscription_id,
                            "DISPLAY_NAME": subscription_name,
                            "PreTaxCost": f"{row[0]:.2f} {row[2]}",
                            "TAGS": subscription_tags if subscription_tags else "None",
                        } for row in cm_client_query_rows
                    ], indent=4, default=str), end="\n\n\n")

                except Exception as e:
                    print(f"An error occurred: {e}")
                    return {"error": str(e)}

            _thread = threading.Thread(target=_sub_cost_export)
            _thread.start()
            _thread.join()

    return cm_client_query_results


# Pylint: disable=too-many-positional-arguments
def _cost_export_subfunc(
    group_by: str = 'service',
    subscriptions_list_detailed: List[dict[str, Any]] = None,
    start_date: str = None,
    end_date: str = None,
    granularity: str = 'Monthly',
    cm_client: CostManagementClient = None,
    cm_client_query_results = None,
):  # Pylint: disable=too-many-arguments 
    """
    Internal function to fetch Azure costs grouped by a custom dimension.

    Executes cost management queries for each subscription, grouping results
    by the specified dimension (ServiceName or ResourceGroupName). This is
    an internal helper function called by cost_export() when group_by is
    'ServiceName' or 'ResourceGroupName'.

    Args:
        group_by (str, optional):
            Dimension to group costs by. Valid values:
            - 'ServiceName': Group by Azure service name
            - 'ResourceGroupName': Group by resource group
            Defaults to 'service'.

        subscriptions_list_detailed (List[dict[str, Any]]):
            List of subscription dictionaries as returned by list_subs().
            Each dictionary must contain 'Subscription_ID', 'Display_Name',
            and optionally 'Tags'.

        start_date (str):
            Start date in "YYYY,MM,DD" format. Inclusive.

        end_date (str):
            End date in "YYYY,MM,DD" format. Inclusive.

        granularity (str, optional):
            Time granularity for cost aggregation. Valid values:
            - 'Monthly' (default): Monthly aggregated costs
            - 'Daily': Daily cost records

        cm_client (CostManagementClient):
            Pre-initialized Azure CostManagementClient instance.

        cm_client_query_results (list):
            List to append cost records to. Modified in-place.

    Returns:
        List[dict]: Updated cost records list with dimension-level data.

    Note:
        This is an internal function and should not be called directly.
        It uses threading for each subscription query and displays
        progress using rich.live.
    """
    start_date = datetime.datetime.strptime(start_date, "%Y,%m,%d")
    end_date = datetime.datetime.strptime(end_date, "%Y,%m,%d")
    subscription_id = ""
    subscription_name = ""
    subscription_tags = ""
    scope = ""

    for sub in subscriptions_list_detailed:
        subscription_id = sub['Subscription_ID']
        subscription_name = sub['Display_Name']
        subscription_tags = sub.get('Tags', {})
        scope = f"/subscriptions/{subscription_id}"
        
        with Live(Spinner
                ("bouncingBar", text=f"Fetching Azure costs of subscriptions: {subscription_name}({subscription_id})...\n\n"),
                    refresh_per_second=10):
            def _srv_cost_export():
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
                                },
                                grouping=[
                                    models.QueryGrouping(type='Dimension', name=group_by)
                                ]                                 
                            )
                        )
                    )
                    cm_client_query_rows = cm_client_query.rows
                    for row in cm_client_query_rows:
                        time_period = row[1]
                        PreTaxCost = row[0]
                        currency = row[2]
                        
                        cm_client_query_results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "GROUP_BY": currency,
                                "SUBSCRIPTION_ID": subscription_id,
                                "DISPLAY_NAME": subscription_name,
                                "PreTaxCost": f"{PreTaxCost:.2f}",
                                "TAGS": subscription_tags if subscription_tags else "None"
                            }
                        )

                    # Combine results of for loop and print
                    print(json.dumps([
                        {
                            "TIME_PERIOD": row[1],
                            "GROUP_BY": currency,
                            "SUBSCRIPTION_ID": subscription_id,
                            "DISPLAY_NAME": subscription_name,
                            "PreTaxCost": f"{row[0]:.2f}",
                            "TAGS": subscription_tags if subscription_tags else "None",
                        } for row in cm_client_query_rows
                    ], indent=4, default=str), end="\n\n\n")

                except Exception as e:
                    print(f"An error occurred: {e}")
                    return {"error": str(e)}

            # progress.update(task, advance=1)
            _thread = threading.Thread(target=_srv_cost_export)
            _thread.start()
            _thread.join()
    return cm_client_query_results
