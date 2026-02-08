# 🔷 Azure Cost Export API

This section documents the Azure cost export endpoints for the eraXplor API.

## 📋 API Information

- **API Name**: eraXplor API
- **Version**: 2.0.0
- **Base URL**: `http://localhost:8000`

---

## 🏠 Root Endpoint

- **GET** `/` - Welcome message

---

## 📖 Interactive Documentation

- **GET** `/docs` - Swagger UI
- **GET** `/redoc` - ReDoc

---

## 🔷 Azure Cost Export Endpoints

### POST `/azure/cost/export`

Export Azure cost data using JSON request body.

**Request Body:**
```json
{
  "start_date": "2025-08-01",
  "end_date": "2025-10-30",
  "granularity": "Monthly",
  "group_by": "subscription"
}
```

**Parameters:**
- `start_date` (string, optional): Start date in YYYY-MM-DD format. Defaults to 90 days ago.
- `end_date` (string, optional): End date in YYYY-MM-DD format. Defaults to today.
- `granularity` (string, optional): "Monthly" or "Daily". Default: "Monthly"
- `group_by` (string, optional): Group by dimension. Options: "subscription", "ServiceName", "ResourceGroupName". Default: "subscription"

### GET `/azure/cost/export`

Export Azure cost data using query parameters.

**Query Parameters:**
- `start_date` (optional): YYYY-MM-DD format
- `end_date` (optional): YYYY-MM-DD format
- `granularity` (optional): Monthly or Daily
- `group_by` (optional): subscription, ServiceName, or ResourceGroupName

**Example (Specific Subscription):**
```bash
curl "http://localhost:8000/azure/cost/export?start_date=2025-08-01&end_date=2025-10-30&granularity=Monthly"
```

**Example (All Subscriptions):**
```bash
curl "http://localhost:8000/azure/cost/export?granularity=Monthly"
```

---

## 📊 Response Format

```json
{
  "success": true,
  "message": "Azure cost data exported successfully",
  "total_records": 31,
  "cost_data": [
    {
      "TIME_PERIOD": {"start": "2025-08-01", "end": "2025-09-01"},
      "GROUP_BY": "SUBSCRIPTION_ID",
      "SUBSCRIPTION_ID": "12345678-1234-1234-1234-123456789abc",
      "DISPLAY_NAME": "My Subscription",
      "PreTaxCost": "123.45 USD",
      "TAGS": {"environment": "production"}
    }
  ],
  "request_parameters": {
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "Monthly",
    "group_by": "subscription"
  }
}
```

---

## ⚠️ Error Responses

### Azure Module Not Available (503 Service Unavailable)
```json
{
  "error": true,
  "message": "Azure functionality not available. Please install Azure SDK: pip install azure-identity azure-mgmt-costmanagement azure-mgmt-resource"
}
```

### General Error (500 Internal Server Error)
```json
{
  "error": true,
  "message": "Error exporting Azure costs: [detailed error message]"
}
```

### No Subscriptions Found (404)
```json
{
  "error": true,
  "message": "No Azure subscriptions found or accessible"
}
```

---

## 🔧 Testing Azure Endpoint

### Test Azure Endpoint (Specific Subscription)
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription_id": "your-subscription-id",
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "Monthly"
  }'
```

### Test Azure Endpoint (All Subscriptions)
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "Monthly"
  }'
```

---

## 🔐 Authentication Requirements

- Azure CLI logged in (`az login`)
- Or environment variables:
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`
- Appropriate RBAC permissions for Cost Management API

---

## 📝 Dependencies

```
fastapi>=0.68.0
uvicorn>=0.15.0
azure-identity>=1.15.0
azure-mgmt-costmanagement>=1.0.0
azure-mgmt-resource>=23.0.0
```

---

## ✅ Features

✅ Azure Cost Export - Subscription-based cost analysis  
✅ Multi-subscription support  
✅ Multiple grouping dimensions (subscription, ServiceName, ResourceGroupName)  
✅ Flexible date ranges  
✅ Subscription tags support

