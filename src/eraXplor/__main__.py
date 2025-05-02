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

import termcolor
from .utils import (
    banner as generate_banner,
    get_start_date_from_user,
    get_end_date_from_user,
    monthly_account_cost_export,
    get_cost_groupby_key,
    csv_export
)

def main() -> None:
    """Orchestrates & Manage depends of cost export workflow."""
    # Banner
    banner_format, copyright_notice = generate_banner()
    print(f"\n\n {termcolor.colored(banner_format, color="green")}")
    print(f"{termcolor.colored(copyright_notice, color="green")}", end="\n\n")

    # Prompt user for input
    start_date_input = get_start_date_from_user()
    end_date_input = get_end_date_from_user()

    # Prompt for AWS profile name
    aws_profile_name_input = input("Enter your AWS Profile name: ")

    # Prompt for cost group by key
    cost_groupby_key_input = get_cost_groupby_key()

    # Fetch monthly account cost usage
    fetch_monthly_account_cost_usage = monthly_account_cost_export(
        start_date_input, end_date_input,
        aws_profile_name_input,
        cost_groupby_key_input)

    # Export results to CSV
    csv_export(fetch_monthly_account_cost_usage)

if __name__ == "__main__":
    main()
