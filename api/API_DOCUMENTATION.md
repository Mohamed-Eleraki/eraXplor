# 🚀 eraXplor API - Complete Endpoint Documentation

Your eraXplor FastAPI now supports both **AWS** and **Azure** cost exports!

## 📋 **API Information**

- **API Name**: eraXplor API
- **Version**: 1.0.0
- **Description**: A RESTful API for AWS and Azure cost data export
- **Base URL**: `http://localhost:8000`

## 📋 **All Available Endpoints**

### 🏠 **Root Endpoint**
- **GET** `/` - Welcome message

### 📖 **Built-in FastAPI Documentation**
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative documentation (ReDoc)
- **GET** `/openapi.json` - OpenAPI schema

---

## 🟠 **AWS Cost Export Endpoints**

### **POST** `/aws/cost/export`
Export AWS cost data using JSON request body.

**Request Body:**
```json
{
  "start_date": "2025-08-01",          // Optional: YYYY-MM-DD format (defaults to 90 days ago)
  "end_date": "2025-10-30",            // Optional: YYYY-MM-DD format (defaults to today)
  "profile": "default",                // Optional: AWS profile name (default: "default")
  "group_by": "LINKED_ACCOUNT",        // Optional: Cost grouping dimension (default: "LINKED_ACCOUNT")
  "granularity": "MONTHLY"             // Optional: MONTHLY or DAILY (default: "MONTHLY")
}
```

**Group By Options:**
- `LINKED_ACCOUNT` (default)
- `SERVICE` 
- `PURCHASE_TYPE`
- `USAGE_TYPE`
- `LINKED_ACCOUNT-With-SERVICE`
- `LINKED_ACCOUNT-With-PURCHASE_TYPE`
- `LINKED_ACCOUNT-With-USAGE_TYPE`

### **GET** `/aws/cost/export`
Export AWS cost data using query parameters.

**Query Parameters:**
- `start_date` (optional): YYYY-MM-DD format (defaults to 90 days ago)
- `end_date` (optional): YYYY-MM-DD format (defaults to today)
- `profile` (optional): AWS profile name (default: "default")
- `group_by` (optional): Cost grouping dimension (default: "LINKED_ACCOUNT")
- `granularity` (optional): MONTHLY or DAILY (default: "MONTHLY")

**Example:**
```bash
curl "http://localhost:8000/aws/cost/export?start_date=2025-08-01&end_date=2025-10-30&granularity=DAILY"
```

---

## 🔷 **Azure Cost Export Endpoints**

### **POST** `/azure/cost/export`
Export Azure cost data using JSON request body.

**Request Body:**
```json
{
  "subscription_id": "12345678-1234-1234-1234-123456789abc",  // Optional: Azure subscription ID (if omitted, fetches all subscriptions)
  "start_date": "2025-08-01",          // Optional: YYYY-MM-DD format (defaults to 90 days ago)
  "end_date": "2025-10-30",            // Optional: YYYY-MM-DD format (defaults to today)
  "granularity": "Monthly"             // Optional: Monthly or Daily (default: "Monthly")
}
```

**Note**: If `subscription_id` is not provided, the API will fetch cost data for all available subscriptions.

### **GET** `/azure/cost/export`
Export Azure cost data using query parameters.

**Query Parameters:**
- `subscription_id` (optional): Azure subscription ID (if omitted, fetches all subscriptions)
- `start_date` (optional): YYYY-MM-DD format (defaults to 90 days ago)
- `end_date` (optional): YYYY-MM-DD format (defaults to today)
- `granularity` (optional): Monthly or Daily (default: "Monthly")

**Example:**
```bash
curl "http://localhost:8000/azure/cost/export?subscription_id=12345678-1234-1234-1234-123456789abc&granularity=Daily"
```

**Example (All Subscriptions):**
```bash
curl "http://localhost:8000/azure/cost/export?granularity=Monthly"
```

---

## 📊 **Response Format**

Both AWS and Azure endpoints return the same response structure:

```json
---

## 📊 **Response Format**

Both AWS and Azure endpoints return the same response structure:

```json
{
  "success": true,
  "message": "Cost data exported successfully",
  "total_records": 31,
  "cost_data": [
    {
      "TIME_PERIOD": {"Start": "2025-08-01", "End": "2025-09-01"},
      "ID": "891377122503",
      "GROUPBY_FILTER": "Amazon QuickSight", 
      "COST": "3.97 USD"
    }
  ],
  "request_parameters": {
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "profile": "default",           // AWS only
    "subscription_id": "...",       // Azure only
    "group_by": "LINKED_ACCOUNT",   // AWS only
    "granularity": "MONTHLY"
  }
}
```

## ⚠️ **Error Responses**

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
  "message": "Error exporting costs: [detailed error message]"
}
```

---

## 🔧 **Testing Your API**

### Test AWS Endpoint

```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30", 
    "granularity": "DAILY"
  }'
```

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

## 🎯 **Key Differences: AWS vs Azure**

| Feature | AWS | Azure |
|---------|-----|-------|
| **Authentication** | AWS Profile | Azure DefaultAzureCredential |
| **Resource Identifier** | `profile` | `subscription_id` |
| **Granularity Values** | `MONTHLY`, `DAILY` | `Monthly`, `Daily` |
| **Grouping Options** | Multiple (SERVICE, ACCOUNT, etc.) | Subscription-based only |
| **Date Format** | YYYY-MM-DD (API) | YYYY-MM-DD (API), YYYY,MM,DD (internal) |
| **All Resources** | Profile-based | `subscription_id` = null |

---

## 🔐 **Authentication Requirements**

### AWS
- AWS CLI configured with profiles
- Valid AWS credentials in `~/.aws/credentials`
- Appropriate IAM permissions for Cost Explorer API

### Azure
- Azure CLI logged in (`az login`)
- Or environment variables:
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`
- Appropriate RBAC permissions for Cost Management API

---

## 🚀 **Quick Start**

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. **Access Documentation**:
   ```
   http://localhost:8000/docs
   ```

4. **Test Endpoints**:
   - Use Swagger UI at `/docs`
   - Or use curl commands from this documentation

---

## 📝 **Dependencies**

```
fastapi==0.68.0
uvicorn==0.15.0
starlette==0.14.2
boto3>=1.37.0
azure-identity>=1.15.0
azure-mgmt-costmanagement>=1.0.0
azure-mgmt-resource>=23.0.0
```

---

## 🎉 **Your API is Complete!**

✅ **AWS Cost Export** - Full functionality with granularity support  
✅ **Azure Cost Export** - Subscription-based cost analysis with all-subscriptions support  
✅ **Professional Structure** - Following FastAPI best practices  
✅ **Comprehensive Documentation** - Built-in Swagger/ReDoc support  
✅ **Error Handling** - Robust exception management  
✅ **Flexible Parameters** - Support for both GET and POST requests  
✅ **Optional Dependencies** - Graceful degradation when modules unavailable
```

---

## 🔧 **Testing Your API**

### Test AWS Endpoint:
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30", 
    "granularity": "DAILY"
  }'
```

### Test Azure Endpoint:
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

---

## 🎯 **Key Differences: AWS vs Azure**

| Feature | AWS | Azure |
|---------|-----|-------|
| **Authentication** | AWS Profile | Azure DefaultAzureCredential |
| **Resource Identifier** | `profile` | `subscription_id` |
| **Granularity Values** | `MONTHLY`, `DAILY` | `Monthly`, `Daily` |
| **Grouping Options** | Multiple (SERVICE, ACCOUNT, etc.) | Subscription-based only |
| **Date Format** | YYYY-MM-DD (API) | YYYY-MM-DD (API), YYYY,MM,DD (internal) |

---

## 🚀 **Your API is Complete!**

✅ **AWS Cost Export** - Full functionality with granularity support  
✅ **Azure Cost Export** - Subscription-based cost analysis  
✅ **Professional Structure** - Following FastAPI best practices  
✅ **Comprehensive Documentation** - Built-in Swagger/ReDoc support  
✅ **Error Handling** - Robust exception management  
✅ **Flexible Parameters** - Support for both GET and POST requests

**Start your server:** `uvicorn main:app --reload --port 8000`  
**Access documentation:** `http://localhost:8000/docs`