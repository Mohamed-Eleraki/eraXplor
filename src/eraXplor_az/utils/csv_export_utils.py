"""Module for exporting Azure cost data to CSV format."""

import csv
from typing import Any, Dict, List


def csv_export(
    cm_client_query_results: List[Dict[str, Any]],
    filename: str = "az_cost_report.csv",
    ) -> None:
    """Exports Azure cost data to a CSV file with standardized formatting.

    Takes the output from cost_export() _(i.e. depends handle by main)_
    and writes it to a CSV file with consistent column headers and proper formatting.
    The CSV will contain the time period, and associated costs.

    Args:
        cm_client_query_results (list): List of cost data dictionaries as returned
            by cost_export(). Each dictionary should contain:
            - time_period (dict): date as string.
            - COST (str): Cost amount as string.
            
        filename (str, optional): Output filename for the CSV. Defaults to 'az_cost_report.csv'.

    Returns:
        None: Writes directly to file but doesn't return any value.
    """
    # Create a CSV file with write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "TIME_PERIOD",
                "COST",
            ]
        )
        for row in cm_client_query_results:
            time_period = row["TIME_PERIOD"]
            cost = row.get("COST")
            writer.writerow([time_period, cost])
    print(f"\n✅ Data exported to {filename}")
