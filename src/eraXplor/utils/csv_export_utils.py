"""Module for exporting AWS cost data to CSV format."""

import csv
from typing import Any, Dict, List


def csv_export(
    results: List[Dict[str, Any]],
    filename: str = "cost_repot.csv"
    ) -> None:
    """Exports AWS cost data to a CSV file with standardized formatting.

    Takes the output from monthly_account_cost_export() _(i.e. depends handle by main)_
    and writes it to a CSV file with consistent column headers and proper formatting.
    The CSV will contain the time period, Account/Service/Purchase_type/Usage_type,
    and associated costs.

    Args:
        fetch_monthly_account_cost_usage (list): List of cost data dictionaries as returned
            by monthly_account_cost_export(). Each dictionary should contain:
            - time_period (dict): With 'Start' and 'End' keys
            - [<account_id | service name>] (str): AWS account ID | service name
            - account_cost (str): Cost amount as string
        filename (str, optional): Output filename for the CSV. Defaults to 'cost_report.csv'.

    Returns:
        None: Writes directly to file but doesn't return any value.
    """
    # Create a CSV file with write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Start Date",
                "End Date",
                "Account/Service/Purchase_type/Usage_type",
                "Cost",
            ]
        )
        for row in results:
            time_period = row["time_period"]
            name = row.get("account_id") or row.get("service_name")
            cost = row.get("account_cost") or row.get("service_cost")
            writer.writerow([time_period["Start"], time_period["End"], name, cost])
    print(f"\n✅ Data exported to {filename}")
