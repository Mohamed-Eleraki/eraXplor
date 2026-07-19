# MCP Interface

This section documents the HTTP-based MCP endpoints exposed by eraXplor for portal and agent integrations.

---

## Overview

The MCP surface is designed to make the existing AWS and Azure workflows available through lightweight tool discovery and invocation routes. It is intended for clients that want to interact with eraXplor without directly calling the CLI or bespoke API routes.

## Run locally

From the repository root, run the following commands to test the MCP endpoints on your machine:

```bash
python -m pip install -e .
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

If you prefer to run it without installing the package, export the source directory first:

```bash
export PYTHONPATH=src
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Once the server is running, verify it responds:

```bash
curl http://localhost:8000/mcp/tools
```

## Available Endpoints

### Discover tools

- **GET** `/mcp/tools`
- Returns the list of registered MCP tools and their input schemas.

### Invoke a tool

- **POST** `/mcp/invoke`
- Accepts a JSON body containing the target tool name and its arguments.

---

## Example: list tools

```bash
curl http://localhost:8000/mcp/tools
```

Example response:

```json
[
  {
    "name": "eraXplor.aws_focus_workflow",
    "description": "Configure or download AWS FOCUS export artifacts for cost reporting.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "command": { "type": "string" }
      }
    }
  }
]
```

---

## Example: invoke the AWS workflow

```bash
curl -X POST http://localhost:8000/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "eraXplor.aws_focus_workflow",
    "arguments": {
      "command": "configure",
      "profile": "default",
      "region": "us-east-1",
      "stack_name": "CID-DataExports-Source",
      "granularity": "MONTHLY"
    }
  }'
```

---

## Supported Tools

### AWS workflow

- **Tool name**: `eraXplor.aws_focus_workflow`
- **Purpose**: configure the AWS FOCUS stack or download generated parquet files.

### Azure workflow

- **Tool name**: `eraXplor.azure_cost_export`
- **Purpose**: trigger the Azure FOCUS export flow using the existing Azure workflow utilities.

---

## Notes

- The MCP interface is intentionally thin and delegates to the existing provider-specific implementations.
- The same FOCUS-oriented workflow used by the CLI and API is reused here so the behavior stays consistent across entrypoints.
