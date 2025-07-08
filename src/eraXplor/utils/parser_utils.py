"""MOudle for parsing command line arguments for cost export utility."""

import argparse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def parser():
    """Parser for the cost export utility."""
    
    arg_parser = argparse.ArgumentParser(
        description="Export AWS account cost data using AWS Cost Explorer API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
        required=False,
        choices=["LINKED_ACCOUNT", "SERVICE", "PURCHASE_TYPE", "USAGE_TYPE"],
        help=(
            "Cost group by key. "
            "Choose from 'LINKED_ACCOUNT', 'SERVICE', 'PURCHASE_TYPE', 'USAGE_TYPE'. "
        ),
    )
    arg_parser.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        help=(
            "CSV output filename. "
        ),
    )
    arg_parser.add_argument(
        "-G", "--granularity",
        type=str,
        required=False,
        # choices=["DAILY", "MONTHLY", "HOURLY"],
        choices=["DAILY", "MONTHLY"],
        help=(
            "Granularity of the cost data."
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
            start_date_input = date(
                six_months_ago.year, 
                six_months_ago.month, 1).strftime("%Y-%m-%d")
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

def parser_filename_handler(arg_parser: list[argparse.ArgumentParser]) -> str:
    """parser_filename_handler

    Handles the output filename input from the user or sets a default value to "cost_report.csv".

    Args:
        arg_parser (list[argparse.ArgumentParser]): The parser objects.

    Returns:
        str: Returns a `filename` object holds the output filename.
    """
    try:
        if arg_parser.out:
            filename = arg_parser.out
            return filename
        if arg_parser.out is None:  # set default value
            filename = "cost_report.csv"
            return filename
    except ValueError as e:
        print(f"Error parsing output filename: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


def parser_granularity_handler(arg_parser: list[argparse.ArgumentParser]) -> str:
    """parser_granularity_handler

    Handles the granularity input from the user or sets a default value to "monthly".

    Args:
        arg_parser (list[argparse.ArgumentParser]): The parser objects.

    Returns:
        str: Return a `granularity` object holds the granularity value.
    """
    try:
        if arg_parser.granularity:
            granularity = arg_parser.granularity
            return granularity
        if arg_parser.granularity is None:  # set default value
            granularity = "MONTHLY"
            return granularity
    except ValueError as e:
        print(f"Error parsing granularity: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return