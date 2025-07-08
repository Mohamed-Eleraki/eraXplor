"""eraXplor - AWS Cost Export Tool

This is the main entry point for the eraXplor CLI tool, which allows users to export
AWS cost and usage data using AWS Cost Explorer.

Args: 
 --start-date, -s: (Optional) Default value set as six months before.
 
 --end-date, -e: (Optional) Default value set as Today date.
 
 --profile, -p: (Optional) Default value set as default.
 
 --groupby, -g: (Optional) Default value set as LINKED_ACCOUNT.
   The available options are (LINKED_ACCOUNT, SERVICE, PURCHASE_TYPE, USAGE_TYPE)
   
 --out, -o: (Optional) Default value set as `cost_repot.csv`.
 
 --granularity, -G: (Optional) Default value set as `MONTHLY`.
    The available options are (MONTHLY, DAILY)
    
Examples:
    eraXplor --start-date 2025-01-01 --end-date 2025-03-30 \
             --profile my-aws-profile \
             --groupby SERVICE \
             --out output.csv \
             --granularity DAILY

"""

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
    banner_format, copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(banner_format, color="green")}")
    print(f"{termcolor.colored(copyright_notice, color="green")}", end="\n\n")

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
    
    # Export results to CSV
    csv_export(results, filename)

if __name__ == "__main__":
    main()
