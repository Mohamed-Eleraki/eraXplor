# 🟠 AWS Cost Export API

This section documents the AWS cost export endpoints for the eraXplor API.

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

## 🟠 AWS Cost Export Endpoints

### POST `/aws/cost/export`

Export AWS cost data using JSON request body.

**Request Body:**
```json
{
  "start_date": "2025-08-01",
  "end_date": "2025-10-30",
  "profile": "default",
  "group_by": "LINKED_ACCOUNT",
  "granularity": "MONTHLY"
}
```

**Parameters:**
- `start_date` (string, optional): Start date in YYYY-MM-DD format. Defaults to 90 days ago.
- `end_date` (string, optional): End date in YYYY-MM-DD format. Defaults to today.
- `profile` (string, optional): AWS profile name. Default: "default"
- `group_by` (string, optional): Cost grouping dimension. Default: "LINKED_ACCOUNT"
- `granularity` (string, optional): "MONTHLY" or "DAILY". Default: "MONTHLY"

**Group By Options:**
- `LINKED_ACCOUNT` (default)
- `SERVICE`
- `PURCHASE_TYPE`
- `USAGE_TYPE`
- `LINKED_ACCOUNT-With-SERVICE`
- `LINKED_ACCOUNT-With-PURCHASE_TYPE`
- `LINKED_ACCOUNT-With-USAGE_TYPE`

---

### GET `/aws/cost/export`

Export AWS cost data using query parameters.

**Query Parameters:**
- `start_date` (optional): YYYY-MM-DD format
- `end_date` (optional): YYYY-MM-DD format
- `profile` (optional): AWS profile name
- `group_by` (optional): Cost grouping dimension
- `granularity` (optional): MONTHLY or DAILY

**Example:**
```bash
curl "http://localhost:8000/aws/cost/export?start_date=2025-08-01&end_date=2025-10-30&granularity=DAILY"
```

---

## 📊 Response Format

```json
{
  "success": true,
  "message": "AWS cost data exported successfully",
  "total_records": 31,
  "cost_data": [
    {
      "TIME_PERIOD": {"start": "2025-08-01", "end": "2025-09-01"},
      "ID": "891377122503",
      "GROUPBY_FILTER": "Amazon QuickSight",
      "COST": "3.97 USD"
    }
  ],
  "request_parameters": {
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "profile": "default",
    "group_by": "LINKED_ACCOUNT",
    "granularity": "MONTHLY"
  }
}
```

---

## ⚠️ Error Responses

### General Error (500 Internal Server Error)
```json
{
  "error": true,
  "message": "Error exporting AWS costs: [detailed error message]"
}
```

---

## 🔧 Testing AWS Endpoint

```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "DAILY"
  }'
```

---

## 🔐 Authentication Requirements

- AWS CLI configured with profiles
- Valid AWS credentials in `~/.aws/credentials`
- Appropriate IAM permissions for Cost Explorer API

---

## 📝 Dependencies

```
fastapi>=0.68.0
uvicorn>=0.15.0
boto3>=1.37.0
```

---

## ✅ Features

✅ AWS Cost Export - Full functionality with granularity support  
✅ Multiple grouping dimensions  
✅ Flexible date ranges  
✅ Support for AWS profiles

