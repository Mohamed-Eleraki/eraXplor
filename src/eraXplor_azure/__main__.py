"""eraXplor - Azure Cost Export Tool

This is the main entry point for the eraXplor_azure CLI tool, which allows users to export
Azure cost and usage data using Azure CostManagementClient client.

Command Line Arguments:
  --start-date, -s DATE    Start date in YYYY,MM,DD format. 
                           Default: 3 months prior
                           
  --end-date, -e DATE      End date in YYYY,MM,DD format.
                           Default: Today date.
                           
  --subscription-id, -S SUBSCRIPTION_ID  Azure subscription ID for cost export.
                           
  --out, -o FILENAME       Output CSV filename.
                           Default: `az_cost_report.csv`
                           
  --granularity, -G GRANULARITY   Time granularity. Options:
                           - Monthly (default)
                           - Daily

Examples:
  1. Basic usage with default settings:
     eraXplor-azure -S SUBSCRIPTION_ID
  
  2. Custom date range and profile:
     eraXplor-azure -s 2025,01,01 -e 2025,03,30 -S SUBSCRIPTION_ID

Notes:
    - Ensure that the environment is properly authenticated with Azure using `DefaultAzureCredential`.
    - Date strings must follow the exact "YYYY,MM,DD" format to avoid parsing errors.
    - Depending on the size of the date range and granularity, response time may vary.
"""

import json
import termcolor
from eraXplor_azure.utils.banner_utils import banner as generate_banner
from eraXplor_azure.utils.parser_utils import parser
from eraXplor_azure.utils.cost_export_utils import cost_export
from eraXplor_azure.utils.cost_export_utils import subs_cost_export
from eraXplor_azure.utils.csv_export_utils import csv_export

def main() -> None:
    """Orchestrates & Manage depends of cost export workflow."""

    # Banner
    banner_format, copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(banner_format, color="green")}")
    print(f"{termcolor.colored(copyright_notice, color="green")}", end="\n\n")

    # Fetch Parsed parameters by command line
    arg_parser = parser().parse_args()
    start_date_input = arg_parser.start_date
    end_date_input = arg_parser.end_date
    subscription_id_input = arg_parser.subscription_id
    granularity_input = arg_parser.granularity
    filename_input = arg_parser.out

    subscriptions_list_detailed, subscriptions_with_tags_list = subs_cost_export()
    
    # Parsing data to cost export func
    cm_client_query_results = cost_export(
        subscription_id=subscription_id_input,
        subscriptions_list_detailed=subscriptions_list_detailed,
        start_date=start_date_input,
        end_date=end_date_input,
        granularity=granularity_input,
    )

    # print(json.dumps(cm_client_query_results, indent=4, default=str), end="\n\n\n")

    csv_export(cm_client_query_results=cm_client_query_results, filename=filename_input)

if __name__ == "__main__":
    main()
