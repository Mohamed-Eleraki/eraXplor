from datetime import datetime, timedelta

# Use FastAPI but without Pydantic models - just basic endpoints
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import mcp_server

# Import settings from config
from api.app.core.config import settings

from core.services.aws.utils.aws_focus_export_stack_utils import deploy_focus_stack
from core.services.aws.utils.aws_focus_fetch import download_parquet_files

try:
    from core.services.azure.utils.azure_focus_export_utils import (
        create_focus_export,
        get_default_billing_account_and_profile_ids,
    )

    AZURE_AVAILABLE = True
except ImportError:  # pragma: no cover - import fallback
    create_focus_export = None
    get_default_billing_account_and_profile_ids = None
    AZURE_AVAILABLE = False

# Create FastAPI app instance (no Pydantic models)
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the eraXplor API"}


@app.get("/mcp/tools")
async def list_mcp_tools():
    """Expose MCP tool metadata for the portal and agent clients."""
    return mcp_server.registry.list_tools()


@app.post("/mcp/invoke")
async def invoke_mcp_tool(request: Request):
    """Invoke an MCP tool through an HTTP endpoint for portal integrations."""
    try:
        body = await request.json()
    except Exception:
        body = {}

    tool_name = body.get("tool")
    arguments = body.get("arguments", {})
    if not tool_name:
        return JSONResponse(
            {"error": True, "message": "Missing required field 'tool'"},
            status_code=400,
        )

    result = await mcp_server.registry.invoke(tool_name, **arguments)
    return result


@app.post("/aws/focus/run")
async def aws_focus_run_post(request: Request):
    """
    Run AWS FOCUS workflow using POST body.

    Request Body Parameters:
    - command (str, optional): "configure" or "download" (default: "configure")
    - profile (str, optional): AWS profile name (default: "default")
    - region (str, optional): AWS region (default: "us-east-1")
    - stack_name (str, optional): CloudFormation stack name (default: "CID-DataExports-Source")
    - granularity (str, optional): FOCUS time granularity for configure only
      ("HOURLY", "DAILY", "MONTHLY"; default: "MONTHLY")
    """
    try:
        try:
            body = await request.json()
        except Exception:
            body = {}

        command = body.get("command", "configure")
        profile = body.get("profile", "default")
        region = body.get("region", "us-east-1")
        stack_name = body.get("stack_name", "CID-DataExports-Source")
        granularity = body.get("granularity", "MONTHLY")

        if command == "configure":
            stack_result = deploy_focus_stack(
                stack_name=stack_name,
                profile_name=profile,
                region=region,
                focus_time_granularity=granularity,
            )
            return {
                "success": True,
                "command": command,
                "message": "AWS FOCUS stack configured successfully",
                "result": stack_result,
            }

        if command == "download":
            files = download_parquet_files(
                profile_name=profile,
                region=region,
                stack_name=stack_name,
            )
            return {
                "success": True,
                "command": command,
                "message": "AWS FOCUS parquet files downloaded successfully",
                "total_files": len(files),
                "files": files,
            }

        return JSONResponse(
            {
                "error": True,
                "message": "Invalid command. Use 'configure' or 'download'.",
            },
            status_code=400,
        )

    except ValueError as e:
        return JSONResponse(
            {"error": True, "message": str(e)},
            status_code=400,
        )
    except Exception as e:
        print(f"Error running AWS FOCUS command: {str(e)}")
        return JSONResponse(
            {"error": True, "message": f"Error running AWS FOCUS command: {str(e)}"},
            status_code=500,
        )


@app.get("/aws/focus/run")
async def aws_focus_run_get(
    command: str = "configure",
    profile: str = "default",
    region: str = "us-east-1",
    stack_name: str = "CID-DataExports-Source",
    granularity: str = "MONTHLY",
):
    """
    Run AWS FOCUS workflow using query parameters.

    Query Parameters:
    - command (str): "configure" or "download"
    - profile (str): AWS profile name
    - region (str): AWS region
    - stack_name (str): CloudFormation stack name
    - granularity (str): FOCUS time granularity for configure only
    """
    try:
        if command == "configure":
            stack_result = deploy_focus_stack(
                stack_name=stack_name,
                profile_name=profile,
                region=region,
                focus_time_granularity=granularity,
            )
            return {
                "success": True,
                "command": command,
                "message": "AWS FOCUS stack configured successfully",
                "result": stack_result,
            }

        if command == "download":
            files = download_parquet_files(
                profile_name=profile,
                region=region,
                stack_name=stack_name,
            )
            return {
                "success": True,
                "command": command,
                "message": "AWS FOCUS parquet files downloaded successfully",
                "total_files": len(files),
                "files": files,
            }

        return JSONResponse(
            {
                "error": True,
                "message": "Invalid command. Use 'configure' or 'download'.",
            },
            status_code=400,
        )

    except ValueError as e:
        return JSONResponse(
            {"error": True, "message": str(e)},
            status_code=400,
        )
    except Exception as e:
        print(f"Error running AWS FOCUS command: {str(e)}")
        return JSONResponse(
            {"error": True, "message": f"Error running AWS FOCUS command: {str(e)}"},
            status_code=500,
        )


@app.post("/azure/cost/export")
async def export_azure_costs_post(request: Request):
    """
    Export Azure cost data using POST request with JSON body.

    Request Body Parameters:
    - start_date (str, optional): Start date in YYYY-MM-DD format
    - end_date (str, optional): End date in YYYY-MM-DD format
    - granularity (str, optional): Time granularity - "Monthly" or "Daily" (default: "Monthly")
    - group_by (str, optional): Group by dimension - "subscription", "ServiceName", or "ResourceGroupName" (default: "subscription")

    Assumes Azure credentials are already configured in the environment.
    """
    # Check if Azure module is available
    if not AZURE_AVAILABLE:
        return JSONResponse(
            {
                "error": True,
                "message": "Azure functionality not available. Please install Azure SDK: "
                "pip install azure-identity azure-mgmt-costmanagement azure-mgmt-resource",
            },
            status_code=503,
        )
    try:
        # Parse JSON body if present
        try:
            body = await request.json()
        except Exception:
            body = {}

        # Extract parameters with defaults
        start_date = body.get("start_date")
        end_date = body.get("end_date")
        granularity = body.get("granularity", "Monthly")
        group_by = body.get("group_by", "subscription")

        # Set default dates if not provided (Azure format: YYYY,MM,DD)
        if not start_date:
            default_start = (datetime.now() - timedelta(days=90)).strftime("%Y,%m,%d")
            start_date = default_start
        else:
            # Convert from YYYY-MM-DD to YYYY,MM,DD format for Azure
            start_date = start_date.replace("-", ",")

        if not end_date:
            default_end = datetime.now().strftime("%Y,%m,%d")
            end_date = default_end
        else:
            # Convert from YYYY-MM-DD to YYYY,MM,DD format for Azure
            end_date = end_date.replace("-", ",")

        if create_focus_export is None or get_default_billing_account_and_profile_ids is None:
            return JSONResponse(
                {"error": True, "message": "Azure export utilities are not available in this environment."},
                status_code=503,
            )

        billing_ids = get_default_billing_account_and_profile_ids()
        export_result = create_focus_export(
            billing_account_id=billing_ids["billing_account_id"],
            billing_profile_id=billing_ids["billing_profile_id"],
            subscription_id="",
            resource_group_name="focus-data-export-rg",
            storage_account_name="focusdataexportstorage",
            container_name="focusdataexportcontainer",
            folder_name="focusdataexportfolder",
            granularity=granularity,
        )

        response_data = {
            "success": True,
            "message": "Azure FOCUS export flow has been triggered through the existing Azure workflow utilities.",
            "result": export_result,
            "request_parameters": {
                "start_date": start_date.replace(",", "-"),  # Convert back for response
                "end_date": end_date.replace(",", "-"),  # Convert back for response
                "granularity": granularity,
                "group_by": group_by,
            },
        }

        return response_data

    except Exception as e:
        print(f"Error exporting Azure costs: {str(e)}")
        return JSONResponse(
            {"error": True, "message": f"Error exporting Azure costs: {str(e)}"},
            status_code=500,
        )


@app.get("/azure/cost/export")
async def export_azure_costs_get(
    start_date: str = None,
    end_date: str = None,
    granularity: str = "Monthly",
    group_by: str = "subscription",
):
    """
    Export Azure cost data using GET request with query parameters.

    Query Parameters:
    - start_date (str, optional): Start date in YYYY-MM-DD format
    - end_date (str, optional): End date in YYYY-MM-DD format
    - granularity (str, optional): Time granularity - "Monthly" or "Daily" (default: "Monthly")
    - group_by (str, optional): Group by dimension - "subscription", "ServiceName", or "ResourceGroupName" (default: "subscription")

    Assumes Azure credentials are already configured in the environment.
    """
    # Check if Azure module is available
    if not AZURE_AVAILABLE:
        return JSONResponse(
            {
                "error": True,
                "message": "Azure functionality not available. Please install Azure SDK: "
                "pip install azure-identity azure-mgmt-costmanagement azure-mgmt-resource",
            },
            status_code=503,
        )
    try:
        # Set default dates if not provided (Azure format: YYYY,MM,DD)
        if not start_date:
            default_start = (datetime.now() - timedelta(days=90)).strftime("%Y,%m,%d")
            start_date = default_start
        else:
            # Convert from YYYY-MM-DD to YYYY,MM,DD format for Azure
            start_date = start_date.replace("-", ",")

        if not end_date:
            default_end = datetime.now().strftime("%Y,%m,%d")
            end_date = default_end
        else:
            # Convert from YYYY-MM-DD to YYYY,MM,DD format for Azure
            end_date = end_date.replace("-", ",")

        if create_focus_export is None or get_default_billing_account_and_profile_ids is None:
            return JSONResponse(
                {"error": True, "message": "Azure export utilities are not available in this environment."},
                status_code=503,
            )

        billing_ids = get_default_billing_account_and_profile_ids()
        export_result = create_focus_export(
            billing_account_id=billing_ids["billing_account_id"],
            billing_profile_id=billing_ids["billing_profile_id"],
            subscription_id="",
            resource_group_name="focus-data-export-rg",
            storage_account_name="focusdataexportstorage",
            container_name="focusdataexportcontainer",
            folder_name="focusdataexportfolder",
            granularity=granularity,
        )

        response_data = {
            "success": True,
            "message": "Azure FOCUS export flow has been triggered through the existing Azure workflow utilities.",
            "result": export_result,
            "request_parameters": {
                "start_date": start_date.replace(",", "-"),  # Convert back for response
                "end_date": end_date.replace(",", "-"),  # Convert back for response
                "granularity": granularity,
                "group_by": group_by,
            },
        }

        return response_data

    except Exception as e:  # Pylint: disable=broad-except
        print(f"Error exporting Azure costs: {str(e)}")
        return JSONResponse(
            {"error": True, "message": f"Error exporting Azure costs: {str(e)}"},
            status_code=500,
        )

