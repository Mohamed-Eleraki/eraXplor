import asyncio
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api import mcp_server
from api.main import app


def test_aws_focus_tool_returns_success(monkeypatch):
    def fake_deploy_focus_stack(**kwargs):
        return {"status": "configured", **kwargs}

    def fake_download_parquet_files(**kwargs):
        return ["file1.parquet", "file2.parquet"]

    monkeypatch.setattr(mcp_server, "deploy_focus_stack", fake_deploy_focus_stack)
    monkeypatch.setattr(mcp_server, "download_parquet_files", fake_download_parquet_files)

    result = asyncio.run(
        mcp_server.run_aws_focus_workflow(
            command="configure",
            profile="default",
            region="us-east-1",
            stack_name="CID-DataExports-Source",
            granularity="MONTHLY",
        )
    )

    assert result["success"] is True
    assert result["command"] == "configure"
    assert result["result"]["status"] == "configured"


def test_aws_focus_tool_normalizes_run_alias_and_granularity(monkeypatch):
    def fake_deploy_focus_stack(**kwargs):
        return {"status": "configured", **kwargs}

    monkeypatch.setattr(mcp_server, "deploy_focus_stack", fake_deploy_focus_stack)

    result = asyncio.run(
        mcp_server.run_aws_focus_workflow(
            command="run",
            profile="default",
            region="us-east-1",
            stack_name="CID-DataExports-Source",
            granularity="daily",
        )
    )

    assert result["success"] is True
    assert result["command"] == "configure"
    assert result["result"]["focus_time_granularity"] == "DAILY"


def test_azure_cost_tool_normalizes_aliases(monkeypatch):
    def fake_get_billing_ids():
        return {"billing_account_id": "acct-1", "billing_profile_id": "profile-1"}

    def fake_create_focus_export(**kwargs):
        return {"status": "configured", **kwargs}

    monkeypatch.setattr(mcp_server, "get_default_billing_account_and_profile_ids", fake_get_billing_ids)
    monkeypatch.setattr(mcp_server, "azure_create_focus_export", fake_create_focus_export)

    result = asyncio.run(
        mcp_server.run_azure_cost_export(
            start_date="2025-01-01",
            end_date="2025-03-30",
            granularity="daily",
            group_by="subscription",
            subscription_id="sub-123",
            command="run",
        )
    )

    assert result["success"] is True
    assert result["request_parameters"]["granularity"] == "Daily"
    assert result["request_parameters"]["command"] == "configure"
    assert result["result"]["status"] == "configured"


def test_azure_download_tool_returns_success(monkeypatch):
    def fake_download_azure_parquet_files(**kwargs):
        return ["/tmp/file.parquet"]

    monkeypatch.setattr(mcp_server, "download_azure_parquet_files", fake_download_azure_parquet_files)

    result = asyncio.run(
        mcp_server.run_azure_cost_export(
            command="download",
            storage_account_name="storageacct",
            container_name="container",
            folder_name="folder",
        )
    )

    assert result["success"] is True
    assert result["command"] == "download"
    assert result["total_files"] == 1


def test_azure_cost_tool_returns_success(monkeypatch):
    def fake_get_billing_ids():
        return {"billing_account_id": "acct-1", "billing_profile_id": "profile-1"}

    def fake_create_focus_export(**kwargs):
        return {"status": "configured", **kwargs}

    monkeypatch.setattr(mcp_server, "get_default_billing_account_and_profile_ids", fake_get_billing_ids)
    monkeypatch.setattr(mcp_server, "azure_create_focus_export", fake_create_focus_export)

    result = asyncio.run(
        mcp_server.run_azure_cost_export(
            start_date="2025-01-01",
            end_date="2025-03-30",
            granularity="Monthly",
            group_by="subscription",
            subscription_id="sub-123",
            command="configure",
        )
    )

    assert result["success"] is True
    assert result["result"]["status"] == "configured"


def test_mcp_http_endpoint_lists_tools():
    client = TestClient(app)
    response = client.get("/mcp/tools")

    assert response.status_code == 200
    tools = response.json()
    aws_tool = next(tool for tool in tools if tool["name"] == "eraXplor.aws_focus_workflow")
    azure_tool = next(tool for tool in tools if tool["name"] == "eraXplor.azure_cost_export")

    assert aws_tool["inputSchema"]["properties"]["command"]["enum"] == ["configure", "download"]
    assert azure_tool["inputSchema"]["properties"]["command"]["enum"] == ["configure", "download", "export"]
