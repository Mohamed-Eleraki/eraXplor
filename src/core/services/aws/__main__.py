"""eraXplor - AWS Cost Export Tool

The official CLI interface for exporting AWS cost and usage data via AWS Cost Explorer API.
Provides flexible filtering, grouping, and output options for cost analysis.

Command Line Arguments:
  --start-date, -s DATE    Start date in YYYY-MM-DD format. 
                           Default: 3 months prior
                           
  --end-date, -e DATE      End date in YYYY-MM-DD format.
                           Default: Current date
                           
  --profile, -p PROFILE    AWS credential profile name.
                           Default: 'default'
                           
  --groupby, -g DIMENSION  Cost grouping dimension. Options:
                           - LINKED_ACCOUNT (default)
                           - SERVICE
                           - PURCHASE_TYPE 
                           - USAGE_TYPE
                           - LINKED_ACCOUNT-With-SERVICE
                           - LINKED_ACCOUNT-With-PURCHASE_TYPE
                           - LINKED_ACCOUNT-With-USAGE_TYPE
                           
  --out, -o FILENAME       Output CSV filename.
                           Default: 'cost_report_<timestamp>.csv'
                           
  --granularity, -G GRAN   Time granularity. Options:
                           - MONTHLY (default)
                           - DAILY

Examples:
  1. Basic usage with default settings:
     eraXplor-aws
  
  2. Custom date range and profile:
     eraXplor-aws -s 2025-01-01 -e 2025-03-30 -p production
  
  3. Service-level breakdown with daily granularity:
     eraXplor-aws -g SERVICE -G DAILY -o service_costs.csv
  
  4. Account+Service combined analysis:
     eraXplor-aws -g LINKED_ACCOUNT-With-SERVICE

Notes:
  - Requires AWS credentials configured via CLI or IAM role
  - Date range cannot exceed 14 months per AWS limitations
  - Output files contain unblended costs in USD
"""

import json
import termcolor
from .utils.csv_export_utils import csv_export
from .utils.cost_export_utils import monthly_account_cost_export
from .utils.banner_utils import banner as generate_banner
from .utils.parser_utils import (
    parser,
    parser_start_date_handler,
    parser_end_date_handler,
    parser_profile_handler,
    parser_groupby_handler,
    parser_filename_handler,
    parser_granularity_handler,
)

def main() -> None:
    """Orchestrates & Manage depends of cost export workflow."""
    # Banner
    _banner_format, _copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(_banner_format, color="green")}")
    print(f"{termcolor.colored(_copyright_notice, color="green")}", end="\n\n")

    # fetch Parsed parameters by command line
    arg_parser = parser().parse_args()

    # Select start date handler
    start_date_input = parser_start_date_handler(arg_parser)

    # Select end date handler
    end_date_input = parser_end_date_handler(arg_parser)

    # Select profile name
    aws_profile_name_input = parser_profile_handler(arg_parser)

    # Select cost groupby key
    cost_groupby_key_input = parser_groupby_handler(arg_parser)
    
    # Select output filename
    filename = parser_filename_handler(arg_parser)
    
    # check granularity
    granularity = parser_granularity_handler(arg_parser)
    
    # Fetch monthly account cost usage
    results = monthly_account_cost_export(
        start_date_input, end_date_input,
        aws_profile_name_input,
        cost_groupby_key_input,
        granularity)
    
    print(json.dumps(results, indent=4, default=str), end="\n\n\n")
    
    # Export results to CSV
    csv_export(results, filename)

if __name__ == "__main__":
    main()
