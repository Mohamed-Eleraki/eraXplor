import sys
import os
from datetime import datetime, timedelta

# Use FastAPI but without Pydantic models - just basic endpoints
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Import settings from config
from app.core.config import settings

# Add the src directory to Python path to import eraXplor modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.services.aws.utils.aws_focus_export_stack_utils import deploy_focus_stack
from core.services.aws.utils.aws_focus_fetch import download_parquet_files

# Try to import Azure module - make it optional
try:
    from core.services.azure.utils.cost_export_utils import cost_export as azure_cost_export
    from core.services.azure.utils.cost_export_utils import list_subs

    AZURE_AVAILABLE = True
except ImportError as e:
    print(f"Azure module not available: {e}")
    print("Azure endpoints will return an error message")
    azure_cost_export = None
    list_subs = None
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

        print(f"Fetching Azure cost data from {start_date} to {end_date}")
        print(f"Granularity: {granularity}, Group by: {group_by}")

        # Fetch subscriptions first because the Azure export helper expects them.
        subscriptions_list_detailed = list_subs()
        if not subscriptions_list_detailed:
            return JSONResponse(
                {"error": True, "message": "No Azure subscriptions found or accessible"},
                status_code=404,
            )

        # Call eraXplor Azure cost_export function
        cost_data = azure_cost_export(
            group_by=group_by,
            subscriptions_list_detailed=subscriptions_list_detailed,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
        )

        # Handle case where Azure function returns None
        if cost_data is None:
            cost_data = []
            print("No cost data returned from Azure function")

        print(f"Retrieved {len(cost_data)} cost records")

        response_data = {
            "success": True,
            "message": "Azure cost data exported successfully",
            "total_records": len(cost_data),
            "cost_data": cost_data,
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

        print(f"Fetching Azure cost data from {start_date} to {end_date}")
        print(f"Granularity: {granularity}, Group by: {group_by}")

        # Fetch subscriptions first because the Azure export helper expects them.
        subscriptions_list_detailed = list_subs()
        if not subscriptions_list_detailed:
            return JSONResponse(
                {"error": True, "message": "No Azure subscriptions found or accessible"},
                status_code=404,
            )

        # Call eraXplor Azure cost_export function
        cost_data = azure_cost_export(
            group_by=group_by,
            subscriptions_list_detailed=subscriptions_list_detailed,
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
        )

        # Handle case where Azure function returns None
        if cost_data is None:
            cost_data = []
            print("No cost data returned from Azure function")

        print(f"Retrieved {len(cost_data)} cost records")

        response_data = {
            "success": True,
            "message": "Azure cost data exported successfully",
            "total_records": len(cost_data),
            "cost_data": cost_data,
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

