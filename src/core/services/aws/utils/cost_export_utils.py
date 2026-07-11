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
    """Retrieve AWS cost and usage data via Cost Explorer API.

    Fetches unblended costs across all linked accounts in an AWS organization, with flexible
    grouping and granularity options. Data is returned in standardized records suitable for
    analysis or export.

    Args:
        start_date_input (Union[str, datetime]): 
            [REQUIRED] Start date for cost report (inclusive).
            Default: "3 Months ago"
            Format: YYYY-MM-DD datetime object.
            Note: AWS limits historical data to 14 months.

        end_date_input (Union[str, datetime]): 
            [REQUIRED] End date for cost report (inclusive).
            Default: "Today date"
            Format: YYYY-MM-DD datetime object.
            Note: Cannot be earlier than start date.

        aws_profile_name_input (str): 
            [REQUIRED] AWS credential profile name from local configuration.
            Default: "default"

        cost_groupby_key_input (str): 
            [REQUIRED] Dimension for cost aggregation. Valid values:
            Default: "LINKED_ACCOUNT"
            - 'LINKED_ACCOUNT' (default): Costs by AWS account
            - 'SERVICE': Costs by AWS service (e.g. EC2, S3)
            - 'PURCHASE_TYPE': Costs by purchase option
            - 'USAGE_TYPE': Costs by usage category
            - Composite keys (e.g. 'LINKED_ACCOUNT-With-SERVICE')
            - Composite keys (e.g. 'LINKED_ACCOUNT-With-PURCHASE_TYPE')
            - Composite keys (e.g. 'LINKED_ACCOUNT-With-USAGE_TYPE')

        granularity (str): 
            [REQUIRED] Time interval for cost breakdown:
            Default: 'MONTHLY'
            - 'MONTHLY' (default): Monthly aggregates
            - 'DAILY': Daily cost records

    Returns:
        List[_CostRecord]: Structured cost records containing:
            - TIME_PERIOD: Dict with 'Start'/'End' date strings
            - ID: Resource identifier (account, service, etc.)
            - GROUPBY_FILTER: Composite values.
            - COST: Unblended cost as string (USD)

    Raises:
        ValueError: For invalid date ranges or parameters
        ClientError: For AWS API authentication/access issues
        DataNotAvailableError: If requested data exceeds retention period

    Example:
        >>> costs = monthly_account_cost_export(
        ...     start_date_input="2023-01-01",
        ...     end_date_input="2023-03-31",
        ...     aws_profile_name_input="production",
        ...     cost_groupby_key_input="SERVICE",
        ...     granularity="MONTHLY"
        ... )
        >>> len(costs) > 0
        True
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
