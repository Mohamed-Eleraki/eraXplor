"""
eraXplor_azure Utility Module

Exports all utility functions with type annotations for documentation.
This module serves as the central export point for the eraXplor_azure package,
providing access to the core functionality for Azure cost export operations.

The module includes:
    - banner: Generates application banner and copyright information
    - parser: Parses command-line arguments for the cost export tool
    - cost_export: Fetches Azure cost data using the Cost Management API

Version: 3.2.0

Example:
    >>> from eraXplor_azure.utils import banner, parser, cost_export
    >>> banner_format, copyright_notice = banner()
"""

from .banner_utils import banner
from .parser_utils import parser
from .cost_export_utils import cost_export
from .cost_export_utils import list_subs


__version__ = "3.2.0"

__all__ = [
    'banner',
    'parser',
    'cost_export',
    'list_subs',
]

# Add module-level type hints for MkDocs
banner: callable
parser: callable
cost_export: callable
list_subs: callable


def __dir__():
    """
    Return list of exported names for autocomplete and documentation tools.

    Returns:
        list: List of public API names available in this module.
    """
    return __all__
