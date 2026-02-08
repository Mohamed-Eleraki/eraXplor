# Azure API Reference

This section provides the API reference documentation for Azure cost export endpoints.

## Interactive Documentation

### Swagger UI

- **URL**: `/docs`
- **Features**: Request/response testing, parameter exploration

### ReDoc

- **URL**: `/redoc`
- **Features**: Sidebar navigation, endpoint discovery

## API Version

- **Version**: 2.0.0
- **Base Path**: `/api/v2`

## Azure Endpoints

### Root

- `GET /` - Welcome message

### Cost Export

- `POST /azure/cost/export` - Export Azure costs with JSON body
- `GET /azure/cost/export` - Export Azure costs with query parameters

## Authentication

- Azure CLI authentication (`az login`)
- Azure subscription access
- Cost Management API permissions

## Rate Limiting

Azure Cost Management has its own quotas - no built-in limiting.


