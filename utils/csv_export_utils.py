import csv
from typing import List, Dict, Any, Optional
from .cost_export_utils import monthly_account_cost_export

def csv_export(
    fetch_monthly_account_cost_usage: List[Dict[str, Any]], 
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
    # Define CSV headers (column names)
    fieldnames = ["Start Date", "End Date", "Account ID", "Cost"]
            
    # Create a CSV file with write mode
    with open(filename, mode="w", newline="") as csvfile:
        
        # Write headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write each row of data
        for result in fetch_monthly_account_cost_usage:
            # print(f"time_period': {result['time_period']}")
            # print(f"account_id': {result['account_id']}")
            # print(f"account_cost': {result['account_cost']}") 
            
            writer.writerow({
                "Start Date": result["time_period"]["Start"],
                "End Date": result["time_period"]["End"],
                "Account ID": result["account_id"],
                "Cost": result["account_cost"]
            })
    print(f"✅ Data exported to {filename}")
    
# help(csv_export)