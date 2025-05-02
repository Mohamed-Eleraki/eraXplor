"""Module to retrieve AWS account cost data using AWS Cost Explorer API."""

from datetime import datetime
from typing import Dict, List, TypedDict, Union

import boto3


def get_cost_groupby_key():
    """Iteratively prompts the user to select a cost group by key."""
    while True:
        try:
            # Prompt user for input
            cost_groupby_key_input = input(
                """Enter the cost group by key:
    Enter [1] to list by 'LINKED_ACCOUNT' -> Default
    Enter [2] to list by 'SERVICE'
    Enter [3] to list by 'PURCHASE_TYPE'
    Enter [4] to list by 'USAGE_TYPE'
    Press Enter for 'LINKED_ACCOUNT' -> Default:\n"""
            ).strip()

            # use default if empty
            if cost_groupby_key_input == "":
                cost_groupby_key_object = "1"
                print("Defaulting to 'LINKED_ACCOUNT'")
            else:
                cost_groupby_key_object = cost_groupby_key_input

            # Ensure input is valid
            if cost_groupby_key_object not in ["1", "2", "3", "4"]:
                print("Invalid selection. Please enter [1], [2], [3] or [4].")
                continue
            # Return the valid selection
            return int(cost_groupby_key_object)

        except KeyboardInterrupt:
            print("\nUser interrupted. Exiting")
            break


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
    cost_groupby_key_input: int = 1,
) -> List[CostRecord]:
    """Retrieves AWS account cost data for a specified time period using AWS Cost Explorer.

    Fetches the unblended costs for all linked accounts in an AWS organization for a given
    date range, grouped by account ID and returned in monthly granularity.

    Args:
        start_date_input (str): The start date of the cost report in YYYY-MM-DD format.
        end_date_input (str): The end date of the cost report in YYYY-MM-DD format.
        aws_profile_name_input (str): The name of the AWS profile to use for authentication,
            as configured in the local AWS credentials file.

    Returns:
        list: A list of dictionaries containing cost data, where each dictionary has:
            - time_period (dict): Contains 'Start' and 'End' dates for the time period
            - account_id (str): The AWS account ID
            - account_cost (str): The unblended cost amount as a string

    Raises:
        botocore.exceptions.ClientError: If there are AWS API authorization or parameter issues
        botocore.exceptions.ProfileNotFound: If the specified AWS profile doesn't exist
    """
    profile_session = boto3.Session(profile_name=str(aws_profile_name_input))
    ce_client = profile_session.client("ce")

    # if condition determine the type of groupby key
    results = []
    if cost_groupby_key_input == 1:
        # group by account ID
        account_cost_usage = ce_client.get_cost_and_usage(
            TimePeriod={"Start": str(start_date_input), "End": str(end_date_input)},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[  # group the result based on account ID
                {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"}
            ],
        )
        for item in account_cost_usage["ResultsByTime"]:
            time_period = item["TimePeriod"]
            for group in item["Groups"]:
                account_id = group["Keys"][0]
                account_cost = group["Metrics"]["UnblendedCost"]["Amount"]
                results.append(
                    {
                        "time_period": time_period,
                        "account_id": account_id,
                        "account_cost": account_cost,
                    }
                )
    elif cost_groupby_key_input == 2:
        account_cost_usage = ce_client.get_cost_and_usage(
            TimePeriod={"Start": str(start_date_input), "End": str(end_date_input)},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[  # group the result based on service
                {"Type": "DIMENSION", "Key": "SERVICE"}
            ],
        )
        for item in account_cost_usage["ResultsByTime"]:
            time_period = item["TimePeriod"]
            for group in item["Groups"]:
                service_name = group["Keys"][0]
                service_cost = group["Metrics"]["UnblendedCost"]["Amount"]
                results.append(
                    {
                        "time_period": time_period,
                        "service_name": service_name,
                        "service_cost": service_cost,
                    }
                )
    elif cost_groupby_key_input == 3:
        account_cost_usage = ce_client.get_cost_and_usage(
            TimePeriod={"Start": str(start_date_input), "End": str(end_date_input)},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "PURCHASE_TYPE"}],
        )
        for item in account_cost_usage["ResultsByTime"]:
            time_period = item["TimePeriod"]
            for group in item["Groups"]:
                service_name = group["Keys"][0]
                service_cost = group["Metrics"]["UnblendedCost"]["Amount"]
                results.append(
                    {
                        "time_period": time_period,
                        "service_name": service_name,
                        "service_cost": service_cost,
                    }
                )
    elif cost_groupby_key_input == 4:
        account_cost_usage = ce_client.get_cost_and_usage(
            TimePeriod={"Start": str(start_date_input), "End": str(end_date_input)},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "USAGE_TYPE"}],
        )
        for item in account_cost_usage["ResultsByTime"]:
            time_period = item["TimePeriod"]
            for group in item["Groups"]:
                service_name = group["Keys"][0]
                service_cost = group["Metrics"]["UnblendedCost"]["Amount"]
                results.append(
                    {
                        "time_period": time_period,
                        "service_name": service_name,
                        "service_cost": service_cost,
                    }
                )
    return results
