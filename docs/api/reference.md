# API Reference

This section provides auto-generated API reference documentation for the eraXplor API.

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

## OpenAPI Schema

The API is built on the OpenAPI 3.0 specification and provides:

- Complete endpoint documentation
- Request/response schemas
- Parameter definitions
- Error response examples

## API Version

- **Current Version**: 2.0.0
- **Base Path**: `/api/v1`

## Authentication

The eraXplor API uses AWS and Azure CLI credentials for authentication:

- **AWS**: Credentials configured via `~/.aws/credentials` file
- **Azure**: Azure CLI authentication (`az login`)

## Rate Limiting

- No built-in rate limiting (relies on underlying cloud provider limits)
- AWS Cost Explorer has its own quotas
- Azure Cost Management has its own quotas


