""" eraXplor - AWS Cost Export Tool

Main entry point with type-annotated workflow functions.

Examples:
    >>> python3 main.py  #doctest: +SKIP 
    Enter a start date value with YYYY-MM-DD format: 2025-1-1  #doctest: +SKIP 
    Enter a end date value with YYYY-MM-DD format: 2025-3-30  #doctest: +SKIP 
    Enter your AWS Profile name:  #doctest: +SKIP 
    dummy_profile  #doctest: +SKIP
"""
import termcolor
# Add the utils directory system path
# sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
# from date_utils import get_start_date_from_user, get_end_date_from_user
# from cost_export_utils import monthly_account_cost_export
# from csv_export_utils import csv_export
# from banner_utils import banner
from .utils import (
    banner as generate_banner,  # avoiding naming conflicts with the banner var name
    get_start_date_from_user,
    get_end_date_from_user,
    monthly_account_cost_export,
    get_cost_groupby_key,
    csv_export
)

def main() -> None:
    """Orchestrates the cost export workflow with type hints."""
    # Banner
    banner, copyright = generate_banner()
    print(f"\n\n {termcolor.colored(banner, color="green")}")
    print(f"{termcolor.colored(copyright, color="green")}", end="\n\n")
    
    start_date_input = get_start_date_from_user()
    end_date_input = get_end_date_from_user()
    aws_profile_name_input = input("Enter your AWS Profile name: ")
    cost_groupby_key_input = get_cost_groupby_key()
    fetch_monthly_account_cost_usage = monthly_account_cost_export(start_date_input, end_date_input, aws_profile_name_input, cost_groupby_key_input)
    # print(json.dumps(fetch_monthly_account_cost_usage, indent=4, default=str))  # print all
    # print(fetch_monthly_account_cost_usage[0]['account_id'])  # print account id 
    
    csv_export(fetch_monthly_account_cost_usage)  # pass results to csv func
    
if __name__ == "__main__":
    main()
