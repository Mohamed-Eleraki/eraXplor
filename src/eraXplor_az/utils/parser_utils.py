"""Module for parsing command line arguments for cost export utility"""

import argparse
from datetime import datetime, timedelta

def _get_default_start_date():
    today = datetime.today()
    # Go back approx 3 months (~90 days); not always accurate for month boundaries
    three_months_ago = today - timedelta(days=90)
    return three_months_ago.strftime("%Y,%m,%d")

def parser():
    """Parser for the cost export utility."""
    
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
        "-S", "--subscription-id",
        type=str,
        required=True,
        help="Azure subscription ID for cost export.",
    )
    arg_parser.add_argument(
        "-g", "--granularity",
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
