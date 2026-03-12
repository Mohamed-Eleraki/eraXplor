"""
Module for exporting Azure cost data to CSV format.

This module provides functionality to write Azure cost and usage data to CSV files
with standardized formatting. It is typically used in conjunction with the
cost_export() function to persist cost data for further analysis or reporting.

The CSV output includes the following columns:
    - TIME_PERIOD: Date or date range for the cost record
    - GROUP_BY: The grouping dimension used (e.g. 'SUBSCRIPTION_ID', currency)
    - SUBSCRIPTION_ID: The Azure subscription ID
    - DISPLAY_NAME: The subscription display name
    - PreTaxCost: The cost amount with currency
    - TAGS: Subscription tags (if available)

Example:
    >>> from eraXplor_azure.utils.cost_export_utils import cost_export, list_subs
    >>> from eraXplor_azure.utils.csv_export_utils import csv_export
    >>> subs = list_subs()
    >>> costs = cost_export(
    ...     group_by='subscription',
    ...     subscriptions_list_detailed=subs,
    ...     start_date='2025,01,01',
    ...     end_date='2025,01,31'
    ... )
    >>> csv_export(cm_client_query_results=costs, filename='cost_report.csv')
"""

import csv
from typing import Any, Dict, List


def csv_export(
    cm_client_query_results: List[Dict[str, Any]],
    filename: str,
    ) -> None:
    """
    Exports Azure cost data to a CSV file with standardized formatting.

    Takes the output from cost_export() and writes it to a CSV file with
    consistent column headers and proper formatting. The CSV will contain
    cost records with their associated metadata including time period,
    grouping information, subscription details, and tags.

    Args:
        cm_client_query_results (List[Dict[str, Any]]):
            List of cost data dictionaries as returned by cost_export().
            Each dictionary should contain the following keys:
            - TIME_PERIOD (str): Date or date range for the cost record
            - GROUP_BY (str): The grouping dimension used
            - SUBSCRIPTION_ID (str): The Azure subscription ID
            - DISPLAY_NAME (str): The subscription display name
            - PreTaxCost (str): Cost amount formatted with currency
            - TAGS (dict or str): Subscription tags or "None"

        filename (str):
            Output filename for the CSV file. Defaults to 'az_cost_report.csv'
            if not specified. The file will be created in the current working
            directory unless a path is included in the filename.

    Returns:
        None: This function writes directly to file and prints a confirmation
              message to stdout, but does not return any value.

    Raises:
        IOError: If the file cannot be created or written to.
        KeyError: If required keys are missing from the input dictionaries.

    Example:
        >>> from eraXplor_azure.utils.csv_export_utils import csv_export
        >>> costs = [
        ...     {
        ...         'TIME_PERIOD': {'Start': '2025-01-01', 'End': '2025-01-31'},
        ...         'GROUP_BY': 'SUBSCRIPTION_ID',
        ...         'SUBSCRIPTION_ID': 'sub-12345',
        ...         'DISPLAY_NAME': 'My Subscription',
        ...         'PreTaxCost': '123.45 USD',
        ...         'TAGS': {'env': 'production'}
        ...     }
        ... ]
        >>> csv_export(cm_client_query_results=costs, filename='report.csv')
        Data exported to report.csv

    Notes:
        - The function uses UTF-8 encoding for proper handling of special characters.
        - A confirmation message is printed to console upon successful export.
        - Existing files with the same name will be overwritten.
    """
    # Create a CSV file with write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "TIME_PERIOD",
                "GROUP_BY",
                "SUBSCRIPTION_ID",
                "DISPLAY_NAME",
                "PreTaxCost",
                "TAGS",
            ]
        )
        for row in cm_client_query_results:
            time_period = row["TIME_PERIOD"]
            group_by = row["GROUP_BY"]
            subscription_id = row["SUBSCRIPTION_ID"]
            display_name = row["DISPLAY_NAME"]
            PreTaxCost = row.get("PreTaxCost")
            tags = row.get("TAGS", {})
            writer.writerow(
                [time_period, group_by, subscription_id, display_name, PreTaxCost, tags]
                )
    print(f"\n Data exported to {filename}")
