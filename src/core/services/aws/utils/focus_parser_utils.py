"""Moudle for parsing command line arguments for cost export utility."""

import argparse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


def parser():
    """Parser for the cost export utility."""

    arg_parser = argparse.ArgumentParser(
        description="Export AWS account cost data using AWS Cost Explorer API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "-p",
        "--profile",
        type=str,
        required=False,
        default="default",
        help="AWS profile name to use for authentication.",
    )
    arg_parser.add_argument(
        "-r",
        "--region",
        type=str,
        required=False,
        default="us-east-1",
        help="AWS region to use for authentication.",
    )
    arg_parser.add_argument(
        "-g",
        "--granularity",
        type=str,
        required=False,
        choices=["HOURLY", "DAILY", "MONTHLY"],
        default="MONTHLY",
        help="Time granularity of the cost data.",
    )
    arg_parser.add_argument(
        "-s",
        "--stack-name",
        type=str,
        required=False,
        default="CID-DataExports-Source",
        help="CloudFormation stack name for the CID Data Exports deployment.",
    )
    return arg_parser


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
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None

def parser_stack_name_handler(arg_parser: list[argparse.ArgumentParser]) -> str:
    """parser_stack_name_handler

    Handles the stack name input from the user or sets a default value to
    "CID-DataExports-Source".

    Args:
        arg_parser (list[argparse.ArgumentParser]): The parser objects.

    Returns:
        str: Returns a `stack_name` object holds the CloudFormation stack name.
    """
    try:
        if arg_parser.stack_name:
            stack_name = arg_parser.stack_name
            return stack_name
        if arg_parser.stack_name is None:  # set default value
            stack_name = "CID-DataExports-Source"
            return stack_name
    except ValueError as e:
        print(f"Error parsing stack name: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_region_handler(arg_parser: list[argparse.ArgumentParser]) -> str:
    """parser_region_handler

    Handles the region input from the user or sets a default value to "us-east-1".

    Args:
        arg_parser (list[argparse.ArgumentParser]): The parser objects.

    Returns:
        str: Returns a `aws_region_input` object holds the region name.
    """
    try:
        if arg_parser.region:
            aws_region_input = arg_parser.region
            return aws_region_input
        if arg_parser.region is None:  # set default value
            aws_region_input = "us-east-1"
            return aws_region_input
    except ValueError as e:
        print(f"Error parsing AWS region: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


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
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None
