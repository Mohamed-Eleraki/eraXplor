"""
Utility module for Azure FOCUS resource provisioning argument parsing.

This module provides command-line argument parsing functionality for configuring
Azure resource creation settings used by the eraXplor Azure FOCUS export tool.
It defines a parser for parameters such as resource group name, location,
storage account, container, and folder names, as well as handler functions for
each argument following the same pattern as the AWS parser.

The module includes:
    - parser(): Creates and returns the ArgumentParser instance
    - parser_resource_group_name_handler(): Handles the resource group name argument
    - parser_location_handler(): Handles the location argument
    - parser_storage_account_name_handler(): Handles the storage account name argument
    - parser_container_name_handler(): Handles the container name argument
    - parser_folder_name_handler(): Handles the folder name argument
    - parser_subscription_id_handler(): Handles the subscription ID argument
    - parser_command_handler(): Handles the command argument

Example:
    >>> from eraXplor_azure.utils.azure_focus_parser_utils import parser
    >>> args = parser().parse_args([
    ...     '--resource-group-name', 'focus-data-export-rg',
    ...     '--location', 'eastus'
    ... ])
    >>> args.location
    'eastus'
"""

import argparse


def _normalize_export_format(value: str) -> str:
    """Normalize supported export formats for Azure FOCUS exports."""
    normalized_value = value.lower()
    if normalized_value not in {"parquet", "csv"}:
        raise argparse.ArgumentTypeError(
            "export format must be one of: parquet, csv"
        )
    return normalized_value


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
        -rn, --resource-group-name (str): Name of the resource group to create.
                                          Default: focus-data-export-rg
        -l, --location (str): Azure region for the resources.
                              Default: eastus
        -sn, --storage-account-name (str): Name of the Storage Account to create.
                                           Default: focusdataexportstorage
        -cn, --container-name (str): Name of the Storage Container to create.
                                     Default: focusdataexportcontainer
        -fn, --folder-name (str): Name of the folder to create.
                                  Default: focusdataexportfolder
        -s, --subscription-id (str): Azure Subscription ID.
        -c, --command (str): Run mode: configure resources or download parquet files.
                             Choices: configure, download. Default: configure

    Example:
        >>> from eraXplor_azure.utils.azure_focus_parser_utils import parser
        >>> args = parser().parse_args([
        ...     '--resource-group-name', 'focus-data-export-rg',
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
        default="eastus",
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
    arg_parser.add_argument(
        "-g",
        "--granularity",
        type=str,
        required=False,
        choices=["Hourly", "Daily", "Monthly"],
        default="Monthly",
        help="Time granularity of the exported cost data.",
    )
    arg_parser.add_argument(
        "-ef",
        "--export-format",
        type=_normalize_export_format,
        choices=["parquet", "csv"],
        required=False,
        default="parquet",
        metavar="{parquet,csv}",
        help="Export file format for the FOCUS data. Supported values: parquet, csv.",
    )
    arg_parser.add_argument(
        "-c",
        "--command",
        type=str,
        required=False,
        choices=["configure", "download"],
        default="configure",
        help="Run mode: configure resources or download parquet files.",
    )

    return arg_parser


def parser_resource_group_name_handler(arg_parser: argparse.Namespace) -> str:
    """parser_resource_group_name_handler

    Handles the resource group name input from the user or sets a default value
    to "focus-data-export-rg".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `resource_group_name` string holding the resource group name.
    """
    try:
        if arg_parser.resource_group_name:
            resource_group_name = arg_parser.resource_group_name
            return resource_group_name
        if arg_parser.resource_group_name is None:
            resource_group_name = "focus-data-export-rg"
            return resource_group_name
    except ValueError as e:
        print(f"Error parsing resource group name: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_location_handler(arg_parser: argparse.Namespace) -> str:
    """parser_location_handler

    Handles the location input from the user or sets a default value to "eastus".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `location` string holding the Azure region name.
    """
    try:
        if arg_parser.location:
            location = arg_parser.location
            return location
        if arg_parser.location is None:
            location = "eastus"
            return location
    except ValueError as e:
        print(f"Error parsing location: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_storage_account_name_handler(arg_parser: argparse.Namespace) -> str:
    """parser_storage_account_name_handler

    Handles the storage account name input from the user or sets a default value
    to "focusdataexportstorage".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `storage_account_name` string holding the storage account name.
    """
    try:
        if arg_parser.storage_account_name:
            storage_account_name = arg_parser.storage_account_name
            return storage_account_name
        if arg_parser.storage_account_name is None:
            storage_account_name = "focusdataexportstorage"
            return storage_account_name
    except ValueError as e:
        print(f"Error parsing storage account name: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_container_name_handler(arg_parser: argparse.Namespace) -> str:
    """parser_container_name_handler

    Handles the container name input from the user or sets a default value
    to "focusdataexportcontainer".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `container_name` string holding the container name.
    """
    try:
        if arg_parser.container_name:
            container_name = arg_parser.container_name
            return container_name
        if arg_parser.container_name is None:
            container_name = "focusdataexportcontainer"
            return container_name
    except ValueError as e:
        print(f"Error parsing container name: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_folder_name_handler(arg_parser: argparse.Namespace) -> str:
    """parser_folder_name_handler

    Handles the folder name input from the user or sets a default value
    to "focusdataexportfolder".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `folder_name` string holding the folder name.
    """
    try:
        if arg_parser.folder_name:
            folder_name = arg_parser.folder_name
            return folder_name
        if arg_parser.folder_name is None:
            folder_name = "focusdataexportfolder"
            return folder_name
    except ValueError as e:
        print(f"Error parsing folder name: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_granularity_handler(arg_parser: argparse.Namespace) -> str:
    """parser_granularity_handler

    Handles the granularity input from the user or sets a default value
    to "Monthly".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `granularity` string, either "Daily" or "Monthly".
    """
    try:
        if arg_parser.granularity:
            granularity = arg_parser.granularity
            return granularity
        if arg_parser.granularity is None:
            granularity = "Monthly"
            return granularity
    except ValueError as e:
        print(f"Error parsing granularity: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_subscription_id_handler(arg_parser: argparse.Namespace) -> str:
    """parser_subscription_id_handler

    Handles the subscription ID input from the user.

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `subscription_id` string holding the Azure Subscription ID,
             or None if not provided.
    """
    try:
        if arg_parser.subscription_id:
            subscription_id = arg_parser.subscription_id
            return subscription_id
        return None
    except ValueError as e:
        print(f"Error parsing subscription ID: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_export_format_handler(arg_parser: argparse.Namespace) -> str:
    """Normalize the export-format argument to a supported value."""
    try:
        export_format = getattr(arg_parser, "export_format", None)
        if export_format is None:
            return "parquet"
        return export_format.lower()
    except ValueError as e:
        print(f"Error parsing export format: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None


def parser_command_handler(arg_parser: argparse.Namespace) -> str:
    """parser_command_handler

    Handles command mode input from the user or sets a default value to
    "configure".

    Args:
        arg_parser (argparse.Namespace): The parsed argument namespace.

    Returns:
        str: Returns a `command_mode` string holding the selected command mode.
             Either "configure" (provision backend + export) or "download"
             (fetch parquet files).
    """
    try:
        if arg_parser.command:
            command_mode = arg_parser.command
            return command_mode
        if arg_parser.command is None:
            command_mode = "configure"
            return command_mode
    except ValueError as e:
        print(f"Error parsing command mode: {e}")
        return None
    except Exception as e:  # Pylint: disable=broad-except
        print(f"Unexpected error: {e}")
        return None
