""" eraXport Utility Module

Exports all untility functions with type annotations for documentation.
"""

from .banner_utils import banner
from .cost_export_utils import monthly_account_cost_export
from .cost_export_utils import get_cost_groupby_key
from .csv_export_utils import csv_export
from .date_utils import get_start_date_from_user, get_end_date_from_user

__version__ = "1.0.1"

__all__=[
    'banner',
    'monthly_account_cost_export',
    'get_cost_groupby_key',
    'csv_export',
    'get_start_date_from_user',
    'get_end_date_from_user'
]

# Add module-level type hints for MkDocs
banner: callable
monthly_account_cost_export: callable
get_cost_groupby_key: callable
csv_export:callable
get_start_date_from_user: callable
get_end_date_from_user: callable

def __dir__():
    """For autocomplete and documentation tools"""
    return __all__