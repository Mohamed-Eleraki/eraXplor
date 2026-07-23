"""eraXplor - Azure FOCUS Export Tool

The official CLI interface for deploying and managing Azure FOCUS data export flow.
Provides a single entrypoint that handles dependencies and parameter passing
between the Azure FOCUS components.

Flow Order:
    1. Render banner from shared utils (../utils/banner_utils)
    2. Parse input parameters via azure_focus_parser_utils
    3. Provision backend resources and create FOCUS export via azure_focus_depends
       and azure_focus_export_utils
    4. Download generated parquet files via azure_focus_fetch

Command Line Arguments (from azure_focus_parser_utils):
    --command, -c MODE              Operation mode. Options:
                                    - configure (default)
                                    - download

    --resource-group-name, -rn NAME Resource group name.
                                    Default: 'focus-data-export-rg'

    --location, -l LOCATION         Azure region for the resources.
                                    Default: 'eastus'

    --storage-account-name, -sn NAME  Storage Account name.
                                    Default: 'focusdataexportstorage'

    --container-name, -cn NAME      Blob container name.
                                    Default: 'focusdataexportcontainer'

    --folder-name, -fn NAME         Folder name inside container.
                                    Default: 'focusdataexportfolder'

    --subscription-id, -s ID        Azure Subscription ID.

    --granularity, -g GRAN          Export time granularity. Options:
                                    - Hourly
                                    - Daily
                                    - Monthly (default)

    --export-format, -ef FORMAT     Export file format. Options:
                                    - parquet (default)
                                    - csv
"""

import sys
import termcolor

from core.services.azure.utils.azure_focus_depends import create_resource_group, create_storage_account_container_folder
from core.services.azure.utils.azure_focus_export_utils import (
    create_focus_export,
    get_default_billing_account_and_profile_ids,
)
from core.services.azure.utils.azure_focus_fetch import download_parquet_files
from core.services.azure.utils.azure_focus_parser_utils import (
    parser,
    parser_resource_group_name_handler,
    parser_location_handler,
    parser_storage_account_name_handler,
    parser_container_name_handler,
    parser_folder_name_handler,
    parser_subscription_id_handler,
    parser_granularity_handler,
    parser_export_format_handler,
    parser_command_handler,
)
from core.services.utils.banner_utils import banner as generate_banner

def main() -> None:
    """Orchestrates and manages dependencies of Azure FOCUS export workflow."""
    try:
        # Banner
        _banner_format, _copyright_notice = generate_banner()
        print(f"\n\n {termcolor.colored(_banner_format, color='green')}")
        print(f"{termcolor.colored(_copyright_notice, color='green')}", end="\n\n")

        # Parse CLI args
        arg_parser = parser().parse_args()

        # Resolve parser-managed values
        rg_name_input = parser_resource_group_name_handler(arg_parser)
        location_input = parser_location_handler(arg_parser)
        storage_account_name_input = parser_storage_account_name_handler(arg_parser)
        container_name_input = parser_container_name_handler(arg_parser)
        folder_name_input = parser_folder_name_handler(arg_parser)
        subscription_id_input = parser_subscription_id_handler(arg_parser)
        granularity_input = parser_granularity_handler(arg_parser)
        export_format_input = parser_export_format_handler(arg_parser)
        command_mode = parser_command_handler(arg_parser)

        if command_mode == "configure":
            print("\n=== Running backend provisioning stage ===")
            create_resource_group(
                resource_group_name=rg_name_input,
                location=location_input,
                subscription_id=subscription_id_input,
            )
            create_storage_account_container_folder(
                resource_group_name=rg_name_input,
                location=location_input,
                storage_account_name=storage_account_name_input,
                container_name=container_name_input,
                folder_name=folder_name_input,
                subscription_id=subscription_id_input,
            )
            print("\n=== Running FOCUS export creation stage ===")
            billing_ids = get_default_billing_account_and_profile_ids()
            create_focus_export(
                billing_account_id=billing_ids["billing_account_id"],
                billing_profile_id=billing_ids["billing_profile_id"],
                subscription_id=subscription_id_input,
                resource_group_name=rg_name_input,
                storage_account_name=storage_account_name_input,
                container_name=container_name_input,
                folder_name=folder_name_input,
                granularity=granularity_input,
                export_format=export_format_input,
            )
            print(
                f"FOCUS export configured successfully as {export_format_input.upper()}. "
                "Run again with '--command download' after data is available.",
                end="\n\n",
            )
            return

        if command_mode == "download":
            print("\n=== Running fetch stage for Parquet files ===")
            download_parquet_files(
                storage_account_name=storage_account_name_input,
                container_name=container_name_input,
                folder_name=folder_name_input,
                export_format=export_format_input,
            )
            return

        raise ValueError(
            f"Unsupported command mode '{command_mode}'. "
            "Use '--command configure' or '--command download'."
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(2)
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
