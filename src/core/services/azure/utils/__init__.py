"""
eraXplor_azure Utility Module

Exports all utility functions with type annotations for documentation.
This module serves as the central export point for the eraXplor_azure package,
providing access to the core functionality for Azure FOCUS export operations.

The module includes:
    - banner: Generates application banner and copyright information
    - parser: Parses command-line arguments for the FOCUS export tool
    - FOCUS Export: Functions for creating and managing Azure FOCUS cost exports
    - Resource Management: Functions for creating required Azure resources
Version: 3.3.0

Example:
    >>> from core.services.azure.utils import banner, parser, create_focus_export
    >>> from core.services.azure.utils import get_default_billing_account_and_profile_ids
    >>> banner_format, copyright_notice = banner()
    >>> billing_ids = get_default_billing_account_and_profile_ids()
"""

from core.services.utils.banner_utils import banner
from .azure_focus_parser_utils import parser
from .azure_focus_export_utils import (
    get_billing_accounts,
    get_billing_profiles,
    get_default_billing_account_and_profile_ids,
    build_export_payload,
    create_focus_export,
)
from .azure_focus_depends import (
    create_resource_group,
    create_storage_account_container_folder,
)
from .azure_focus_fetch import download_parquet_files


__version__ = "3.3.0"

__all__ = [
    'banner',
    'parser',
    # FOCUS Export Functions
    'get_billing_accounts',
    'get_billing_profiles',
    'get_default_billing_account_and_profile_ids',
    'build_export_payload',
    'create_focus_export',
    # Resource Management Functions
    'create_resource_group',
    'create_storage_account_container_folder',
    # Fetch Functions
    'download_parquet_files',
]

# Add module-level type hints for MkDocs
banner: callable
parser: callable
get_billing_accounts: callable
get_billing_profiles: callable
get_default_billing_account_and_profile_ids: callable
build_export_payload: callable
create_focus_export: callable
create_resource_group: callable
create_storage_account_container_folder: callable
download_parquet_files: callable


def __dir__():
    """
    Return list of exported names for autocomplete and documentation tools.

    Returns:
        list: List of public API names available in this module.
    """
    return __all__
