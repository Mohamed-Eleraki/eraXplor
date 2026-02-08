"""
Module for parsing command line arguments for the eraXplor_azure cost export utility.

This module provides command-line argument parsing functionality for configuring
the Azure cost export process. It uses argparse to define and parse command-line
arguments including date ranges, grouping dimensions, granularity, and output options.

The module includes:
    - _get_default_start_date(): Calculates default start date (3 months ago)
    - parser(): Creates and returns the ArgumentParser instance

Example:
    >>> from eraXplor_azure.utils.parser_utils import parser
    >>> args = parser().parse_args()
    >>> print(args.start_date)
    2024,10,25
"""

import argparse
from datetime import datetime, timedelta


def _get_default_start_date():
    """
    Calculates a default start date for cost export, approximately 3 months ago.

    This helper function calculates a default start date by subtracting 90 days
    from the current date. The result is formatted as "YYYY,MM,DD" to match
    the expected input format for the cost export tool.

    Returns:
        str: A date string in "YYYY,MM,DD" format representing approximately
             3 months ago from the current date.

    Note:
        - This uses a fixed 90-day offset, which may not accurately reflect
          calendar month boundaries.
        - The date format uses commas as separators (not dashes or slashes).
    """
    today = datetime.today()
    # Go back approx 3 months (~90 days); not always accurate for month boundaries
    three_months_ago = today - timedelta(days=90)
    return three_months_ago.strftime("%Y,%m,%d")


def parser():
    """
    Create and return an ArgumentParser for the eraXplor_azure cost export utility.

    This function creates an argparse.ArgumentParser configured with all command-line
    arguments supported by the eraXplor_azure tool. The parser includes help text,
    default values, and argument choices for validation.

    Returns:
        argparse.ArgumentParser: A configured ArgumentParser instance ready to
                                 parse command-line arguments.

    Command Line Arguments:
        -s, --start-date (str): Start date in YYYY,MM,DD format.
                                Default: ~3 months ago
        -e, --end-date (str): End date in YYYY,MM,DD format.
                              Default: Today's date
        -g, --group-by (str): Cost grouping dimension.
                              Options: subscription (default), ServiceName, ResourceGroupName
        -G, --granularity (str): Time granularity for cost aggregation.
                                Options: Monthly (default), Daily
        -o, --out (str): Output CSV filename.
                        Default: az_cost_report.csv

    Example:
        >>> from eraXplor_azure.utils.parser_utils import parser
        >>> args = parser().parse_args([
        ...     '--start-date', '2025,01,01',
        ...     '--end-date', '2025,01,31',
        ...     '--group-by', 'subscription'
        ... ])
        >>> args.start_date
        '2025,01,01'
        >>> args.granularity
        'Monthly'

    Note:
        - The parser uses ArgumentDefaultsHelpFormatter to show default values in help.
        - All date arguments must follow the "YYYY,MM,DD" format with commas.
        - The --help or -h flag displays all available arguments and their descriptions.
    """
    
    arg_parser = argparse.ArgumentParser(
        description="Export Azure cost data for using Azure Cost Management API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "-s", "--start-date",
        type=str,
        required=False,
        help="Start date for cost export in YYYY,MM,DD format.",
        default=_get_default_start_date(),
    )
    arg_parser.add_argument(
        "-e", "--end-date",
        type=str,
        required=False,
        help="End date for cost export in YYYY,MM,DD format.",
        default=datetime.today().strftime("%Y,%m,%d"),
    )
    arg_parser.add_argument(
        "-g", "--group-by",
        type=str,
        choices=['ServiceName', "subscription", "ResourceGroupName"],
        required=False,
        default='subscription',
        help="Cost grouping dimension (ServiceName, subscription or ResourceGroupName). " \
        "Default is subscription.",
    )
    arg_parser.add_argument(
        "-G", "--granularity",
        type=str,
        choices=['Daily', 'Monthly'],
        default='Monthly',
        help="Granularity of cost data (Daily or Monthly). Default is Monthly.",
    )
    arg_parser.add_argument(
        "-o", "--out",
        type=str,
        required=False,
        default="az_cost_report.csv",
        help="CSV output filename.",
    )
    
    return arg_parser
