# API Reference

This section provides auto-generated API reference documentation for the eraXplor API, extracted directly from the FastAPI application docstrings.

## Interactive Documentation

The eraXplor API provides two interactive documentation interfaces:

### Swagger UI

A user-friendly interface to explore and test the API endpoints.

- **URL**: `/docs`
- **Features**: Request/response testing, parameter exploration, schema viewing

### ReDoc

An alternative documentation interface with a clean, three-panel layout.

- **URL**: `/redoc`
- **Features**: Sidebar navigation, easy endpoint discovery, schema references

## Auto-Generated Reference

::: api.main
    options:
        heading_level: 2
        show_root_heading: true
        members:
            - root
            - export_aws_costs_post
            - export_aws_costs_get
            - export_azure_costs_post
            - export_azure_costs_get

## Authentication

The eraXplor API uses AWS and Azure CLI credentials for authentication:

- **AWS**: Credentials configured via `~/.aws/credentials` file
- **Azure**: Azure CLI authentication (`az login`)

## Rate Limiting

- No built-in rate limiting (relies on underlying cloud provider limits)
- AWS Cost Explorer has its own quotas
- Azure Cost Management has its own quotas

