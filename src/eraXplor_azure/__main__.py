"""
eraXplor - Azure Cost Export Tool

This is the main entry point for the eraXplor_azure CLI tool, which enables users to export
Azure cost and usage data using the Azure Cost Management API.

The tool supports multiple grouping dimensions (subscription, ServiceName, ResourceGroupName)
and provides both daily and monthly cost aggregation granularity.

Command Line Arguments:
  --start-date, -s DATE    Start date in YYYY,MM,DD format.
                           Default: 3 months prior

  --end-date, -e DATE      End date in YYYY,MM,DD format.
                           Default: Today date.

  --group-by, -g GROUPBY   Cost grouping dimension. Options:
                           - subscription (default)
                           - ServiceName
                           - ResourceGroupName

  --granularity, -G GRANULARITY   Time granularity. Options:
                           - Monthly (default)
                           - Daily

  --out, -o FILENAME       Output CSV filename.
                           Default: `az_cost_report.csv`

Examples:
  1. Basic usage with default settings:
     eraXplor-azure

  2. Custom date range:
     eraXplor-azure -s 2025,01,01 -e 2025,03,30

  3. Group by service name with daily granularity:
     eraXplor-azure -g ServiceName -G Daily

  4. Export to custom filename:
     eraXplor-azure -o my_cost_report.csv

Notes:
    - Ensure that the environment is properly authenticated with Azure using `DefaultAzureCredential`.
    - Date strings must follow the exact "YYYY,MM,DD" format to avoid parsing errors.
    - Depending on the size of the date range and granularity, response time may vary.
    - The tool queries all subscriptions accessible by the authenticated principal.
"""

import termcolor
from eraXplor_azure.utils.banner_utils import banner as generate_banner  # pylint: disable=import-error
from eraXplor_azure.utils.parser_utils import parser  # pylint: disable=import-error
from eraXplor_azure.utils.cost_export_utils import cost_export  # pylint: disable=import-error
from eraXplor_azure.utils.cost_export_utils import list_subs  # pylint: disable=import-error
from eraXplor_azure.utils.csv_export_utils import csv_export  # pylint: disable=import-error

def main() -> None:
    """
    Orchestrates and manage the cost export workflow.

    This function serves as the main entry point for the eraXplor_azure CLI tool.
    It coordinates the entire cost export process by:
    1. Displaying the application banner with version information
    2. Parsing command-line arguments for configuration
    3. Retrieving all accessible Azure subscriptions
    4. Fetching cost data using the Azure Cost Management API
    5. Exporting the results to a CSV file

    The function uses the following workflow:
        - generate_banner(): Displays the eraXplor banner
        - parser(): Parses CLI arguments
        - list_subs(): Retrieves subscription details
        - cost_export(): Fetches cost data for all subscriptions
        - csv_export(): Writes results to CSV format

    Returns:
        None: This function does not return a value. It prints output directly
              to the console and writes the cost report to a CSV file.

    Raises:
        Any exceptions raised by the underlying Azure SDK calls or file I/O
        operations are propagated to the caller.

    Example:
        >>> if __name__ == "__main__":
        ...     main()

    Note:
        This function is typically called from the command line and should
        not be imported directly for programmatic use. For programmatic use,
        import and call the individual utility functions directly.
    """

    # Banner
    banner_format, copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(banner_format, color="green")}")
    print(f"{termcolor.colored(copyright_notice, color="green")}", end="\n\n")

    # Fetch Parsed parameters by command line
    arg_parser = parser().parse_args()
    start_date_input = arg_parser.start_date
    end_date_input = arg_parser.end_date
    group_by = arg_parser.group_by
    granularity_input = arg_parser.granularity
    filename_input = arg_parser.out

    # Fetch detailed subscriptions list
    subscriptions_list_detailed = list_subs()
    
    # Parsing data to subscription cost export func
    cm_client_query_results = cost_export(
        group_by=group_by,
        subscriptions_list_detailed=subscriptions_list_detailed,
        start_date=start_date_input,
        end_date=end_date_input,
        granularity=granularity_input,
    )

    # Parsing date to csv_export func
    csv_export(cm_client_query_results=cm_client_query_results, filename=filename_input)

if __name__ == "__main__":
    main()
