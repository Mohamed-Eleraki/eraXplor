import argparse
import json
from typing import Any, Dict, List, Optional

from core.services.aws.utils.aws_focus_export_stack_utils import deploy_focus_stack
from core.services.aws.utils.aws_focus_fetch import download_parquet_files
from core.services.aws.utils.focus_parser_utils import (
    parser_command_handler as aws_parser_command_handler,
    parser_granularity_handler as aws_parser_granularity_handler,
    parser_profile_handler as aws_parser_profile_handler,
    parser_region_handler as aws_parser_region_handler,
    parser_stack_name_handler as aws_parser_stack_name_handler,
)
from core.services.azure.utils.azure_focus_export_utils import (
    create_focus_export as azure_create_focus_export,
    get_default_billing_account_and_profile_ids,
)
from core.services.azure.utils.azure_focus_fetch import download_parquet_files as download_azure_parquet_files
from core.services.azure.utils.azure_focus_parser_utils import (
    parser_command_handler as azure_parser_command_handler,
    parser_container_name_handler,
    parser_folder_name_handler,
    parser_granularity_handler as azure_parser_granularity_handler,
    parser_location_handler,
    parser_resource_group_name_handler,
    parser_storage_account_name_handler,
    parser_subscription_id_handler,
)


try:
    from core.services.azure.utils.azure_focus_fetch import download_parquet_files as download_azure_parquet_files
    from core.services.azure.utils.azure_focus_parser_utils import parser_granularity_handler as azure_parser_granularity_handler

    AZURE_AVAILABLE = True
except ImportError:  # pragma: no cover - import fallback
    download_azure_parquet_files = None
    azure_parser_granularity_handler = None
    AZURE_AVAILABLE = False


def _normalize_azure_granularity(value: Optional[str]) -> str:
    """Normalize common Azure granularity aliases to the values expected by the backend."""
    if value is None:
        return "Monthly"
    normalized = str(value).strip().lower()
    mapping = {
        "hour": "Hourly",
        "hourly": "Hourly",
        "day": "Daily",
        "daily": "Daily",
        "month": "Monthly",
        "monthly": "Monthly",
    }
    return mapping.get(normalized, "Monthly")


def _normalize_azure_command(value: Optional[str]) -> str:
    """Normalize common Azure command aliases to the parser's supported values."""
    if value is None:
        return "configure"
    normalized = str(value).strip().lower()
    if normalized in {"run", "execute", "start", "export"}:
        return "configure"
    if normalized in {"download", "fetch"}:
        return "download"
    return normalized


def _build_aws_tool_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "enum": ["configure", "download"],
                "description": "Choose configure to deploy the AWS FOCUS stack, or download to fetch parquet files.",
            },
            "profile": {
                "type": "string",
                "description": "AWS profile name, default: default",
            },
            "region": {
                "type": "string",
                "description": "AWS region, default: us-east-1",
            },
            "stack_name": {
                "type": "string",
                "description": "CloudFormation stack name, default: CID-DataExports-Source",
            },
            "granularity": {
                "type": "string",
                "enum": ["HOURLY", "DAILY", "MONTHLY"],
                "description": "Time granularity for configure operations.",
            },
        },
        "required": [],
    }


def _build_azure_tool_schema() -> Dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "enum": ["configure", "download", "export"],
                "description": "Choose export behavior for Azure cost data. 'export' is an alias for configure.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date in YYYY-MM-DD format",
            },
            "end_date": {
                "type": "string",
                "description": "End date in YYYY-MM-DD format",
            },
            "granularity": {
                "type": "string",
                "enum": ["Hourly", "Daily", "Monthly"],
                "description": "Time granularity for Azure cost export",
            },
            "group_by": {
                "type": "string",
                "description": "Grouping dimension such as subscription",
            },
            "subscription_id": {
                "type": "string",
                "description": "Azure subscription ID",
            },
        },
        "required": [],
    }


async def run_aws_focus_workflow(
    *,
    command: Optional[str] = None,
    profile: Optional[str] = None,
    region: Optional[str] = None,
    stack_name: Optional[str] = None,
    granularity: Optional[str] = None,
) -> Dict[str, Any]:
    """Expose the AWS FOCUS workflow as a prompt-friendly MCP tool."""
    try:
        normalized_command = (command or "").strip().lower()
        if normalized_command in {"run", "execute"}:
            normalized_command = "configure"

        normalized_granularity = (granularity or "").strip().upper()
        if normalized_granularity in {"HOURLY", "DAILY", "MONTHLY"}:
            pass
        elif normalized_granularity in {"HOUR", "HOURLY"}:
            normalized_granularity = "HOURLY"
        elif normalized_granularity in {"DAY", "DAILY"}:
            normalized_granularity = "DAILY"
        elif normalized_granularity in {"MONTH", "MONTHLY"}:
            normalized_granularity = "MONTHLY"
        else:
            normalized_granularity = "MONTHLY"

        parsed_args = argparse.Namespace(
            profile=profile,
            region=region,
            granularity=normalized_granularity,
            stack_name=stack_name,
            command=normalized_command,
        )
        resolved_command = aws_parser_command_handler(parsed_args) or "configure"
        resolved_profile = aws_parser_profile_handler(parsed_args) or "default"
        resolved_region = aws_parser_region_handler(parsed_args) or "us-east-1"
        resolved_stack_name = aws_parser_stack_name_handler(parsed_args) or "CID-DataExports-Source"
        resolved_granularity = aws_parser_granularity_handler(parsed_args) or "MONTHLY"

        if resolved_command == "configure":
            result = deploy_focus_stack(
                stack_name=resolved_stack_name,
                profile_name=resolved_profile,
                region=resolved_region,
                focus_time_granularity=resolved_granularity,
            )
            if isinstance(result, dict):
                result = {**result, "focus_time_granularity": resolved_granularity}
            return {
                "success": True,
                "command": resolved_command,
                "message": "AWS FOCUS stack configured successfully",
                "result": result,
            }

        if resolved_command == "download":
            files = download_parquet_files(
                profile_name=resolved_profile,
                region=resolved_region,
                stack_name=resolved_stack_name,
            )
            return {
                "success": True,
                "command": resolved_command,
                "message": "AWS FOCUS parquet files downloaded successfully",
                "total_files": len(files),
                "files": files,
            }

        return {
            "success": False,
            "error": True,
            "message": "Invalid command. Use 'configure' or 'download'.",
        }
    except Exception as exc:  # pragma: no cover - exercised via tests
        return {
            "success": False,
            "error": True,
            "message": f"Error running AWS FOCUS command: {exc}",
        }


async def run_azure_cost_export(
    *,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: Optional[str] = None,
    group_by: str = "subscription",
    resource_group_name: Optional[str] = None,
    location: Optional[str] = None,
    storage_account_name: Optional[str] = None,
    container_name: Optional[str] = None,
    folder_name: Optional[str] = None,
    subscription_id: Optional[str] = None,
    command: Optional[str] = None,
) -> Dict[str, Any]:
    """Expose Azure cost export as a prompt-friendly MCP tool."""
    try:
        normalized_command = _normalize_azure_command(command)
        normalized_granularity = _normalize_azure_granularity(granularity)
        parsed_args = argparse.Namespace(
            resource_group_name=resource_group_name,
            location=location,
            storage_account_name=storage_account_name,
            container_name=container_name,
            folder_name=folder_name,
            subscription_id=subscription_id,
            granularity=normalized_granularity,
            command=normalized_command,
        )
        resolved_granularity = azure_parser_granularity_handler(parsed_args) or "Monthly"
        resolved_subscription_id = parser_subscription_id_handler(parsed_args)
        resolved_command = azure_parser_command_handler(parsed_args) or "configure"

        if resolved_command not in {"configure", "download"}:
            return {
                "success": False,
                "error": True,
                "message": "Invalid Azure command. Use 'configure' or 'download'.",
            }

        if resolved_command == "download":
            files = download_azure_parquet_files(
                storage_account_name=storage_account_name or "focusdataexportstorage",
                container_name=container_name or "focusdataexportcontainer",
                folder_name=folder_name or "focusdataexportfolder",
            )
            return {
                "success": True,
                "command": resolved_command,
                "message": "Azure parquet files downloaded successfully",
                "total_files": len(files),
                "files": files,
            }

        if azure_create_focus_export is None or get_default_billing_account_and_profile_ids is None:
            return {
                "success": False,
                "error": True,
                "message": "Azure functionality not available. Please install Azure SDK dependencies.",
            }

        billing_ids = get_default_billing_account_and_profile_ids()
        export_result = azure_create_focus_export(
            billing_account_id=billing_ids["billing_account_id"],
            billing_profile_id=billing_ids["billing_profile_id"],
            subscription_id=resolved_subscription_id or "",
            resource_group_name=parser_resource_group_name_handler(parsed_args) or "focus-data-export-rg",
            storage_account_name=parser_storage_account_name_handler(parsed_args) or "focusdataexportstorage",
            container_name=parser_container_name_handler(parsed_args) or "focusdataexportcontainer",
            folder_name=parser_folder_name_handler(parsed_args) or "focusdataexportfolder",
            granularity=resolved_granularity,
        )

        return {
            "success": True,
            "message": "Azure FOCUS export configured successfully through the existing Azure workflow utilities.",
            "result": export_result,
            "request_parameters": {
                "start_date": start_date,
                "end_date": end_date,
                "granularity": resolved_granularity,
                "group_by": group_by,
                "subscription_id": resolved_subscription_id,
                "command": resolved_command,
            },
        }
    except Exception as exc:  # pragma: no cover - exercised via tests
        return {
            "success": False,
            "error": True,
            "message": f"Error running Azure cost export: {exc}",
        }


class MCPToolRegistry:
    """A lightweight registry so a future MCP transport can discover tools easily."""

    def __init__(self) -> None:
        self.tools = {
            "eraXplor.aws_focus_workflow": {
                "description": "Configure or download AWS FOCUS export artifacts for cost reporting. Use command='configure' to deploy the stack or command='download' to fetch parquet files.",
                "inputSchema": _build_aws_tool_schema(),
                "handler": run_aws_focus_workflow,
            },
            "eraXplor.azure_cost_export": {
                "description": "Export Azure cost data for a date range and grouping. Use command='export' or 'configure' to run the export flow.",
                "inputSchema": _build_azure_tool_schema(),
                "handler": run_azure_cost_export,
            },
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": name,
                "description": spec["description"],
                "inputSchema": spec.get("inputSchema", {}),
            }
            for name, spec in self.tools.items()
        ]

    async def invoke(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        tool = self.tools.get(name)
        if not tool:
            return {"success": False, "error": True, "message": f"Unknown MCP tool: {name}"}
        return await tool["handler"](**kwargs)


registry = MCPToolRegistry()


if __name__ == "__main__":
    print(json.dumps(registry.list_tools(), indent=2))
