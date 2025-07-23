"""Module to retrieve AWS account cost data using AWS Cost Explorer API."""

import threading
from datetime import datetime
from typing import Dict, List, TypedDict, Union
import boto3
from rich.live import Live
from rich.spinner import Spinner


class _CostRecord(TypedDict):
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
) -> List[_CostRecord]:
    """Retrieves AWS account cost data for a specified time period using AWS Cost Explorer.

    Fetches the unblended costs for all linked accounts, services, purchase type, or usage type
    in an AWS organization for a given date range, grouped by account ID and returned in
    monthly granularity.

    Args:
        - start_date_input (str): The start date of the cost report in YYYY-MM-DD format. Default: Six months ago.

        - end_date_input (str): The end date of the cost report in YYYY-MM-DD format. Default: Today.

        - aws_profile_name_input (str): The name of the AWS profile to use for authentication,
            as configured in the local AWS credentials file. Default: 'default'.

        - cost_groupby_key_input (str): The key to group costs by (`LINKED_ACCOUNT`, `SERVICE`,
            `PURCHASE_TYPE`, `USAGE_TYPE`). Default: `LINKED_ACCOUNT`.

        - granularity (str): The granularity of the cost data, either 'MONTHLY' or 'DAILY'. Default: 'MONTHLY'.


    Returns:
        list: A list of dictionaries containing cost data, where each dictionary has:
            - TIME_PERIOD (dict): Contains 'Start' and 'End' dates for the time period.
            - ID (str): The AWS account, service, purchase type, or usage type.
            - COST (str): The unblended cost amount as a string.

    """

    _profile_session = boto3.Session(profile_name=str(aws_profile_name_input))
    _ce_client = _profile_session.client("ce")

    # if condition determine the type of groupby key
    results = []
    with Live(
        Spinner(
            "bouncingBar",
            text=f"Fetching AWS costs grouped by {cost_groupby_key_input}...\n\n",
        ),
        refresh_per_second=10,
    ):

        def _fetch_account():
            if cost_groupby_key_input == "LINKED_ACCOUNT-With-SERVICE":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                        {"Type": "DIMENSION", "Key": "SERVICE"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        service = _group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": service,
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
            if cost_groupby_key_input == "LINKED_ACCOUNT-With-PURCHASE_TYPE":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                        {"Type": "DIMENSION", "Key": "PURCHASE_TYPE"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        purchase_type = _group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": purchase_type,
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
            if cost_groupby_key_input == "LINKED_ACCOUNT-With-USAGE_TYPE":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                        {"Type": "DIMENSION", "Key": "USAGE_TYPE"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        usage_type = _group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": usage_type,
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
            if cost_groupby_key_input == "LINKED_ACCOUNT":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        # usage_type = group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": "NONE",
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
            if cost_groupby_key_input == "SERVICE":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "SERVICE"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        # usage_type = group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": "NONE",
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
            if cost_groupby_key_input == "PURCHASE_TYPE":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "PURCHASE_TYPE"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        # usage_type = group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": "NONE",
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
            if cost_groupby_key_input == "USAGE_TYPE":
                _account_cost_usage = _ce_client.get_cost_and_usage(
                    TimePeriod={
                        "Start": str(start_date_input),
                        "End": str(end_date_input),
                    },
                    # Granularity="MONTHLY",
                    Granularity=granularity,
                    Metrics=["UnblendedCost"],
                    GroupBy=[
                        {"Type": "DIMENSION", "Key": "USAGE_TYPE"},
                    ],
                )
                for _item in _account_cost_usage["ResultsByTime"]:
                    time_period = _item["TimePeriod"]
                    for _group in _item["Groups"]:
                        ID = _group["Keys"][0]
                        # usage_type = group["Keys"][1]
                        cost = float(_group["Metrics"]["UnblendedCost"]["Amount"])
                        currency = _group["Metrics"]["UnblendedCost"]["Unit"]
                        results.append(
                            {
                                "TIME_PERIOD": time_period,
                                "ID": ID,
                                "GROUPBY_FILTER": "NONE",
                                "COST": f"{cost:.2f} {currency}",
                            }
                        )
        # progress.update(task, advance=1)
        _thread = threading.Thread(target=_fetch_account)
        _thread.start()
        _thread.join()
    return results
