""" eraXport Utility Module

Exports all untility functions with type annotations for documentation.
"""

from .csv_export_utils import csv_export
from .cost_export_utils import monthly_account_cost_export
from .banner_utils import banner
from .parser_utils import (
    parser,
    parser_start_date_handler,
    parser_end_date_handler,
    parser_profile_handler,
    parser_groupby_handler,
    parser_filename_handler,
    parser_granularity_handler,
)

__version__ = "2.0.2"

__all__=[
    'banner',
    'monthly_account_cost_export',
    'get_cost_groupby_key',
    'csv_export',
    'get_start_date_from_user',
    'get_end_date_from_user',
    'parser',
    'parser_start_date_handler',
    'parser_end_date_handler',
    'parser_profile_handler',
    'parser_groupby_handler',
    'parser_filename_handler',
    'parser_granularity_handler'
]

# Add module-level type hints for MkDocs
banner: callable
monthly_account_cost_export: callable
get_cost_groupby_key: callable
csv_export:callable
get_start_date_from_user: callable
get_end_date_from_user: callable
parser: callable
parser_start_date_handler: callable
parser_end_date_handler: callable
parser_profile_handler: callable
parser_groupby_handler: callable
parser_filename_handler: callable
parser_granularity_handler: callable

def __dir__():
    """For autocomplete and documentation tools"""
    return __all__
