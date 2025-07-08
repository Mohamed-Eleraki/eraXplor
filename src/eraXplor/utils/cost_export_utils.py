"""Module to retrieve AWS account cost data using AWS Cost Explorer API."""

import threading
from datetime import datetime
from typing import Dict, List, TypedDict, Union
import boto3
from rich.live import Live
from rich.spinner import Spinner

class CostRecord(TypedDict):
    """Class type annotation tool dettermining the List Schema.
    Type definition for a single cost record.
    """

    time_period: Dict[str, str]  # {'Start': str, 'End': str}
    account_id: str
    account_cost: str
    

def monthly_account_cost_export(
    start_date_input: Union[str, datetime],  # str | datetime
    end_date_input: Union[str, datetime],
    aws_profile_name_input: str,
    cost_groupby_key_input: str,
    granularity: str,
) -> List[CostRecord]:
    """Retrieves AWS account cost data for a specified time period using AWS Cost Explorer.

    Fetches the unblended costs for all linked accounts, services, purchase type, or usage type
    in an AWS organization for a given date range, grouped by account ID and returned in 
    monthly granularity.

    Args:
        - start_date_input (str): The start date of the cost report in YYYY-MM-DD format.
        
        - end_date_input (str): The end date of the cost report in YYYY-MM-DD format.
        
        - aws_profile_name_input (str): The name of the AWS profile to use for authentication,
            as configured in the local AWS credentials file.
            
        - cost_groupby_key_input (str): The key to group costs by (`LINKED_ACCOUNT`, `SERVICE`, 
            `PURCHASE_TYPE`, `USAGE_TYPE`)
        
        - granularity (str): The granularity of the cost data, either 'MONTHLY' or 'DAILY'.


    Returns:
        list: A list of dictionaries containing cost data, where each dictionary has:
            - TIME_PERIOD (dict): Contains 'Start' and 'End' dates for the time period.
            - ID (str): The AWS account, service, purchase type, or usage type.
            - COST (str): The unblended cost amount as a string.
            
    """

    profile_session = boto3.Session(profile_name=str(aws_profile_name_input))
    ce_client = profile_session.client("ce")

    # if condition determine the type of groupby key
    results = []
    # if cost_groupby_key_input == "account":
    with Live(Spinner
              ("bouncingBar", text=f"Fetching AWS costs grouped by {cost_groupby_key_input}...\n\n"),
                refresh_per_second=10):
        def fetch_account():
            account_cost_usage = ce_client.get_cost_and_usage(
                TimePeriod={"Start": str(start_date_input), "End": str(end_date_input)},
                # Granularity="MONTHLY",
                Granularity=granularity,
                Metrics=["UnblendedCost"],
                GroupBy=[  # group the result based on account ID
                    {"Type": "DIMENSION", "Key": cost_groupby_key_input}
                ],
            )
            for item in account_cost_usage["ResultsByTime"]:
                time_period = item["TimePeriod"]
                for group in item["Groups"]:
                    ID = group["Keys"][0]
                    cost = group["Metrics"]["UnblendedCost"]["Amount"]
                    results.append(
                        {
                            "TIME_PERIOD": time_period,
                            "ID": ID,
                            "COST": cost,
                        }
                    )
        # progress.update(task, advance=1)
        thread = threading.Thread(target=fetch_account)
        thread.start()
        thread.join()
    return results
