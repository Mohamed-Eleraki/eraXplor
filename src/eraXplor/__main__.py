"""eraXplor - AWS Cost Export Tool

This is the main entry point for the eraXplor CLI tool, which allows users to export
AWS cost and usage data using AWS Cost Explorer.

It provides an interactive command-line workflow to:
1. Prompt the user for a date range (start and end dates).
2. Prompt for an AWS CLI profile to authenticate with.
3. Allow the user to select a cost grouping dimension _(e.g., by account, service,
    Purchase type, Usage type.)_
4. Fetch cost data using the AWS Cost Explorer API.
5. Export the resulting data to a CSV file.

Examples:
    >>> eraXplor
    Enter a start date value with YYYY-MM-DD format: 2025-1-1
    Enter a end date value with YYYY-MM-DD format: 2025-3-30
    Enter your AWS Profile name:  [Profile name]
    Enter the cost group by key:
        Enter [1] to list by 'LINKED_ACCOUNT' -> Default
        Enter [2] to list by 'SERVICE'
        Enter [3] to list by 'PURCHASE_TYPE'
        Enter [4] to list by 'USAGE_TYPE'
        Press Enter for 'LINKED_ACCOUNT' -> Default:

    ✅ Data exported to test_output.csv
"""
import importlib
from datetime import datetime, date
from dateutil.relativedelta import relativedelta 
import termcolor
# from .utils import (
#     banner as generate_banner,
#     get_start_date_from_user,
#     get_end_date_from_user,
#     monthly_account_cost_export,
#     get_cost_groupby_key,
#     csv_export,
# )
from .utils.csv_export_utils import csv_export
from .utils.cost_export_utils import monthly_account_cost_export
from .utils.banner_utils import banner as generate_banner
from .utils.parser_utils import (
    parser,
    parser_start_date_handler,
    parser_end_date_handler,
    parser_profile_handler,
    parser_groupby_handler
)

def main() -> None:
    """Orchestrates & Manage depends of cost export workflow."""
    # Banner
    banner_format, copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(banner_format, color="green")}")
    print(f"{termcolor.colored(copyright_notice, color="green")}", end="\n\n")

    # Parse command line arguments
    arg_parser = parser().parse_args()

    # start date handler
    start_date_input = parser_start_date_handler(arg_parser)

    # end date handler
    end_date_input = parser_end_date_handler(arg_parser)

    # profile name
    aws_profile_name_input = parser_profile_handler(arg_parser)

    cost_groupby_key_input = parser_groupby_handler(arg_parser)
    
    # Fetch monthly account cost usage
    fetch_monthly_account_cost_usage = monthly_account_cost_export(
        start_date_input, end_date_input,
        aws_profile_name_input,
        cost_groupby_key_input)

    # Export results to CSV
    csv_export(fetch_monthly_account_cost_usage)

if __name__ == "__main__":
    main()
