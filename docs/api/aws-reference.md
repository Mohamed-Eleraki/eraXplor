# AWS API Reference

This section provides the API reference documentation for AWS cost export endpoints.

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

## AWS Endpoints

### Root

- `GET /` - Welcome message

### Cost Export

- `POST /aws/cost/export` - Export AWS costs with JSON body
- `GET /aws/cost/export` - Export AWS costs with query parameters

## Authentication

- AWS CLI configured with profiles
- Credentials in `~/.aws/credentials`
- IAM permissions for Cost Explorer API

## Rate Limiting

AWS Cost Explorer has its own quotas - no built-in limiting.


