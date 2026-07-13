"""eraXplor - AWS FOCUS Export Tool

The official CLI interface for deploying and managing AWS FOCUS data export flow.
Provides a single entrypoint that handles dependencies and parameter passing
between the new AWS FOCUS components.

Flow Order:
    1. Render banner from shared utils (../utils/banner_utils)
    2. Parse input parameters via focus_parser_utils
    3. Deploy/update CID FOCUS stack via aws_focus_export_stack_utils
    4. Download generated parquet files via aws_focus_fetch

Command Line Arguments (from focus_parser_utils):
    --command, -c MODE       Operation mode. Options:
                             - configure (default)
                             - download

    --profile, -p PROFILE      AWS credential profile name.
                                                         Default: 'default'

    --region, -r REGION        AWS region name.
                                                         Default: 'us-east-1'

    --stack-name, -s NAME      CloudFormation stack name.
                                                         Default: 'CID-DataExports-Source'

    --granularity, -g GRAN     Export time granularity. Options:
                                                         - HOURLY
                                                         - DAILY
                                                         - MONTHLY (default)
"""

import json
import sys
import termcolor
from ..utils.banner_utils import banner as generate_banner
from .utils.focus_parser_utils import (
    parser,
    parser_command_handler,
    parser_profile_handler,
    parser_region_handler,
    parser_stack_name_handler,
    parser_granularity_handler,
)
from .utils.aws_focus_export_stack_utils import deploy_focus_stack
from .utils.aws_focus_fetch import download_parquet_files


def main() -> None:
    """Orchestrates and manages dependencies of AWS FOCUS export workflow."""
    try:
        # Banner
        _banner_format, _copyright_notice = generate_banner()
        print(f"\n\n {termcolor.colored(_banner_format, color='green')}")
        print(f"{termcolor.colored(_copyright_notice, color='green')}", end="\n\n")

        # Parse CLI args
        arg_parser = parser().parse_args()

        # Resolve parser-managed values
        command_mode = parser_command_handler(arg_parser)
        aws_profile_name_input = parser_profile_handler(arg_parser)
        aws_region_input = parser_region_handler(arg_parser)
        stack_name_input = parser_stack_name_handler(arg_parser)
        focus_time_granularity = parser_granularity_handler(arg_parser)

        if command_mode == "configure":
            # Deploy or update FOCUS export stack
            stack_result = deploy_focus_stack(
                stack_name=stack_name_input,
                profile_name=aws_profile_name_input,
                region=aws_region_input,
                focus_time_granularity=focus_time_granularity,
            )
            print(json.dumps(stack_result, indent=4, default=str), end="\n\n")
            print(
                "FOCUS export configured successfully. "
                "Run again with '--command download' after data is available.",
                end="\n\n",
            )
            return

        if command_mode == "download":
            # Download generated FOCUS parquet files
            downloaded_files = download_parquet_files(
                profile_name=aws_profile_name_input,
                region=aws_region_input,
                stack_name=stack_name_input,
            )
            print(f"Downloaded {len(downloaded_files)} parquet file(s).", end="\n\n")
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
