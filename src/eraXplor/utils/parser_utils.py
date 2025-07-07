"""MOudle for parsing command line arguments for cost export utility."""

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import argparse

def parser():
    """Parser for the cost export utility."""

    arg_parser = argparse.ArgumentParser(
        description="Export AWS account cost data using AWS Cost Explorer API."
    )
    arg_parser.add_argument(
        "-s", "--start-date",
        type=str,
        required=False,
        help="Start date for cost data in YYYY-MM-DD format.",
    )
    arg_parser.add_argument(
        "-e", "--end-date",
        type=str,
        required=False,
        help="End date for cost data in YYYY-MM-DD format.",
    )
    arg_parser.add_argument(
        "-p", "--profile",
        type=str,
        required=False,
        help="AWS profile name to use for authentication.",
    )
    arg_parser.add_argument(
        "-g", "--groupby",
        type=str,
        # choices=[1, 2, 3, 4],
        choices=["account", "service", "purchase_type", "usage_type"],
        # default=1,
        help=(
            "Cost group by key: "
            "1 for 'LINKED_ACCOUNT' (default), "
            "2 for 'SERVICE', "
            "3 for 'PURCHASE_TYPE', "
            "4 for 'USAGE_TYPE'."
        ),
    )
    return arg_parser

def parser_start_date_handler(arg_parser: list[argparse.ArgumentParser]) -> date | str:
    """parser_start_date_handler 

    Hanles the start date input from the user or sets a default value to 6 months ago date.

    Args:
        arg_parser (argparse.ArgumentParser): The parser objects.

    Returns:
        Union[date, str]: Returns a `start_date_input` object provided or a default date.
    """
    try:
        if arg_parser.start_date:
            start_date_input = arg_parser.start_date
            start_date_input = datetime.strptime(start_date_input, "%Y-%m-%d").date()
            return start_date_input
        if arg_parser.start_date is None:  # set default value
            six_months_ago = date.today() - relativedelta(months=6)
            start_date_input = date(six_months_ago.year, six_months_ago.month, 1).strftime("%Y-%m-%d")
            return start_date_input
    except ValueError as e:
        print(f"Error parsing start date: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
    

def parser_end_date_handler(arg_parser: list[argparse.ArgumentParser]) -> date | str:
    """parser_end_date_handler 

    Hanles the end date input from the user or sets a default value to today date.

    Args:
        arg_parser (argparse.ArgumentParser): The parser objects.

    Returns:
        Union[date, str]: Returns a `end_date_input` object provided or a default date.
    """
    try:
        if arg_parser.end_date:
            end_date_input = arg_parser.end_date
            end_date_input = datetime.strptime(end_date_input, "%Y-%m-%d").date()
            return end_date_input
        if arg_parser.end_date is None:  # set default value
            end_date_input = date.today().strftime("%Y-%m-%d")
            return end_date_input
    except ValueError as e:
        print(f"Error parsing end date: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


def parser_profile_handler(arg_parser: list[argparse.ArgumentParser]) -> str:
    """parser_profile

    Handles the profile input from the user or set a default value to "default".

    Args:
        arg_parser (list[argparse.ArgumentParser]): The parser objects.

    Returns:
        str: Returns a `aws_profile_name_input` object holds the profile name.
    """
    try:
         # Check if AWS Profile is provided via command line arguments
        if arg_parser.profile:
            aws_profile_name_input = arg_parser.profile
            return aws_profile_name_input
        if arg_parser.profile is None:  # set default value
            aws_profile_name_input = "default"
            return aws_profile_name_input
    
    except ValueError as e:
        print(f"Error parsing AWS profile: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
   
    
def parser_groupby_handler(arg_parser: list[argparse.ArgumentParser]) -> str:
    """parser_groupby_handler

    Handles the cost group by key input from the user or sets a default value to "LINKED_ACCOUNT".

    Args:
        arg_parser (list[argparse.ArgumentParser]): The parser objects.

    Returns:
        str: Returns a `cost_groupby_key_input` object holds the cost group by key.
    """
    try:
        if arg_parser.groupby:
            cost_groupby_key_input = arg_parser.groupby
            return cost_groupby_key_input
        if arg_parser.groupby is None:  # set default value
            cost_groupby_key_input = "LINKED_ACCOUNT"        
            return cost_groupby_key_input
    except ValueError as e:
        print(f"Error parsing cost group by key: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
