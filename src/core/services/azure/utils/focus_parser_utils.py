"""
Utility module for Azure FOCUS resource provisioning argument parsing.

This module provides command-line argument parsing functionality for configuring
Azure resource creation settings used by the eraXplor Azure FOCUS export tool.
It defines a parser for parameters such as resource group name, location,
storage account, container, and folder names.

The module includes:
    - parser(): Creates and returns the ArgumentParser instance

Example:
    >>> from eraXplor_azure.utils.focus_parser_utils import parser
    >>> args = parser().parse_args([
    ...     '--resource-name', 'focus-data-export-rg',
    ...     '--location', 'eastus'
    ... ])
    >>> args.location
    'eastus'
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
    Create and return an ArgumentParser for Azure FOCUS export resource provisioning.

    This function creates an argparse.ArgumentParser configured with the CLI options
    required to provision Azure resources for the eraXplor Azure FOCUS export utility.
    The parser includes default values and help text for each supported resource
    configuration parameter.

    Returns:
        argparse.ArgumentParser: A configured ArgumentParser instance ready to
                                 parse command-line arguments.

    Command Line Arguments:
        -rn, --resource-name (str): Name of the resource group to create.
                                     Default: focus-data-export-rg
        -l, --location (str): Azure region for the resources.
                              Default: eastus
        -sn, --storage-account-name (str): Name of the Storage Account to create.
                                           Default: focusdataexportstorage
        -cn, --container-name (str): Name of the Storage Container to create.
                                      Default: focusdataexportcontainer
        -fn, --folder-name (str): Name of the folder to create.
                                  Default: focusdataexportfolder

    Example:
        >>> from eraXplor_azure.utils.focus_parser_utils import parser
        >>> args = parser().parse_args([
        ...     '--resource-name', 'focus-data-export-rg',
        ...     '--location', 'eastus',
        ...     '--storage-account-name', 'focusdataexportstorage'
        ... ])
        >>> args.location
        'eastus'

    Note:
        - The parser uses ArgumentDefaultsHelpFormatter to show default values in help.
        - The --help or -h flag displays all available arguments and descriptions.
    """
    
    arg_parser = argparse.ArgumentParser(
        description="Export Azure FOCUS data provisioning configuration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "-rn", "--resource-group-name",
        type=str,
        required=False,
        help="Name of the resource group to create.",
        default="focus-data-export-rg",
    )
    arg_parser.add_argument(
        "-l", "--location",
        type=str,
        required=False,
        help="Azure region for the resources.",
    )
    arg_parser.add_argument(
        "-sn", "--storage-account-name",
        type=str,
        required=False,
        help="Name of the Storage Account to create.",
        default="focusdataexportstorage",
    )
    arg_parser.add_argument(
        "-cn", "--container-name",
        type=str,
        required=False,
        help="Name of the Storage Container to create.",
        default="focusdataexportcontainer",
    )
    arg_parser.add_argument(
        "-fn", "--folder-name",
        type=str,
        required=False,
        help="Name of the folder to create.",
        default="focusdataexportfolder",
    )    
    arg_parser.add_argument(
        "-s", "--subscription-id",
        type=str,
        required=False,
        help="Azure Subscription ID.",
    )
    return arg_parser
