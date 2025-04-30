import csv
from typing import List, Dict, Any, Optional
from .cost_export_utils import monthly_account_cost_export

def csv_export(
    results: List[Dict[str, Any]], 
    filename: str ='cost_repot.csv'
    ) -> None:  # appending typehint
# def csv_export(fetch_monthly_account_cost_usage: Union[List, Dict], filename: str ='cost_repot.csv') -> None:  # appending type hint, accepting List with any value inside or single dict
    """Exports AWS cost data to a CSV file with standardized formatting.

    Takes the output from monthly_account_cost_export() and writes it to a CSV file
    with consistent column headers and proper formatting. The CSV will contain
    the time period, account IDs, and associated costs.

    Args:
        fetch_monthly_account_cost_usage (list): List of cost data dictionaries as returned
            by monthly_account_cost_export(). Each dictionary should contain:
            - time_period (dict): With 'Start' and 'End' keys
            - account_id (str): AWS account ID
            - account_cost (str): Cost amount as string
        filename (str, optional): Output filename for the CSV. Defaults to 'cost_report.csv'.

    Returns:
        None: Writes directly to file but doesn't return any value.

    Raises:
        KeyError: If input data is missing required fields
        IOError: If there are issues writing to the specified file

    Examples:
        >>> test_data = [{
        ...     'time_period': {'Start': '2023-01-01', 'End': '2023-01-31'},
        ...     'account_id': '123456789012',
        ...     'account_cost': '42.50'
        ... }]
        >>> csv_export(test_data, 'test_output.csv')  # doctest: +ELLIPSIS
        ✅ Data exported to test_output.csv

        The file content would be:
        Start Date,End Date,Account ID,Cost
        2023-01-01,2023-01-31,123456789012,42.50
    """
    # Create a CSV file with write mode
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Start Date", "End Date", "Account/Service", "Cost"])
        for row in results:
            time_period = row["time_period"]
            name = row.get("account_id") or row.get("service_name")
            cost = row.get("account_cost") or row.get("service_cost")
            writer.writerow([time_period["Start"], time_period["End"], name, cost])
    print(f"✅ Data exported to {filename}")
        # try:
        #     # Ensure the iterable can be reused
        #     results = list(results)

        #     for result in results:
        #         try:
        #             # First row: Account-level cost info
        #             writer.writerow({
        #                 "Start Date": result["time_period"]["Start"],
        #                 "End Date": result["time_period"]["End"],
        #                 "Account ID": result["account_id"],
        #                 "Cost": result["account_cost"]
        #             })

        #             # Second row: Service-level cost info (if available)
        #             writer.writerow({
        #                 "Start Date": result["time_period"]["Start"],
        #                 "End Date": result["time_period"]["End"],
        #                 "Service Name": result["service_name"],
        #                 "Cost": result["account_cost"]
        #             })

        #         except KeyError as e:
        #             print(f"Missing expected key {e} in result: {result}")
        #             continue  # Skip this result and continue with the next

        # except Exception as e:
        #     print(f"Unexpected error occurred: {e}")
    # print(f"✅ Data exported to {filename}")
# help(csv_export)
