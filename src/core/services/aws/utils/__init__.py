"""eraXplor AWS utility exports for FOCUS workflow."""

from core.services.utils.banner_utils import banner
from .focus_parser_utils import (
    parser,
    parser_command_handler,
    parser_profile_handler,
    parser_region_handler,
    parser_stack_name_handler,
    parser_granularity_handler,
)
from .aws_focus_export_stack_utils import deploy_focus_stack
from .aws_focus_fetch import download_parquet_files


__version__ = "4.0.0"

__all__ = [
    "banner",
    "parser",
    "parser_command_handler",
    "parser_profile_handler",
    "parser_region_handler",
    "parser_stack_name_handler",
    "parser_granularity_handler",
    "deploy_focus_stack",
    "download_parquet_files",
]

banner: callable
parser: callable
parser_command_handler: callable
parser_profile_handler: callable
parser_region_handler: callable
parser_stack_name_handler: callable
parser_granularity_handler: callable
deploy_focus_stack: callable
download_parquet_files: callable


def __dir__():
    """For autocomplete and documentation tools."""
    return __all__
