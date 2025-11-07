# 🧪 eraXplor API Testing Guide

Complete guide to test your eraXplor FastAPI with both AWS and Azure endpoints.

## 🚀 **Step 1: Prerequisites & Setup**

### Check Dependencies
```bash
cd /Users/moeraki/Documents/gitRepoPersonal/eraXplor/api
pip install -r requirements.txt
```

### Required Dependencies
- `fastapi==0.68.0`
- `uvicorn==0.15.0` 
- `boto3>=1.37.0` (AWS)
- `azure-identity>=1.15.0` (Azure)
- `azure-mgmt-costmanagement>=1.0.0` (Azure)
- `azure-mgmt-resource>=23.0.0` (Azure)

### Authentication Setup

**AWS Setup:**
```bash
# Configure AWS CLI with profiles
aws configure --profile default
# Or verify existing configuration
aws configure list --profile default
```

**Azure Setup:**
```bash
# Login to Azure CLI
az login
# Or verify current login
az account show
```

---

## 🚀 **Step 2: Start the API Server**

```bash
cd /Users/moeraki/Documents/gitRepoPersonal/eraXplor/api
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

## 🔍 **Step 3: Test Basic Connectivity**

### Test 1: Root Endpoint
```bash
curl http://localhost:8000/
```
**Expected:** `{"message":"Welcome to the eraXplor API"}`

### Test 2: API Documentation
Open in browser: `http://localhost:8000/docs`
- Interactive Swagger UI
- Try out endpoints directly in browser

### Test 3: Alternative Docs
Open in browser: `http://localhost:8000/redoc`
- Clean ReDoc interface

---

## 🟠 **Step 4: Test AWS Endpoints**

### AWS Test 1: POST with Default Parameters
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{}'
```
*Uses defaults: last 90 days, MONTHLY granularity, LINKED_ACCOUNT grouping*

### AWS Test 2: POST with MONTHLY granularity
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "profile": "default",
    "group_by": "LINKED_ACCOUNT",
    "granularity": "MONTHLY"
  }'
```

### AWS Test 3: POST with DAILY granularity
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-10-01",
    "end_date": "2025-10-15",
    "profile": "default",
    "group_by": "SERVICE",
    "granularity": "DAILY"
  }'
```

### AWS Test 4: GET request with query parameters
```bash
curl "http://localhost:8000/aws/cost/export?start_date=2025-08-01&end_date=2025-10-30&granularity=MONTHLY&group_by=SERVICE"
```

### AWS Test 5: Test different group_by options
```bash
# Test LINKED_ACCOUNT-With-SERVICE grouping
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "group_by": "LINKED_ACCOUNT-With-SERVICE",
    "granularity": "MONTHLY"
  }'
```

---

## 🔷 **Step 5: Test Azure Endpoints**

### Azure Test 1: POST with All Subscriptions (No subscription_id)
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "Monthly"
  }'
```
*This will fetch cost data for all available subscriptions*

### Azure Test 2: POST with Specific Subscription
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription_id": "12345678-1234-1234-1234-123456789abc",
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "Monthly"
  }'
```

### Azure Test 3: POST with Daily granularity
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription_id": "12345678-1234-1234-1234-123456789abc",
    "start_date": "2025-10-01",
    "end_date": "2025-10-15",
    "granularity": "Daily"
  }'
```

### Azure Test 4: GET request (All Subscriptions)
```bash
curl "http://localhost:8000/azure/cost/export?start_date=2025-08-01&end_date=2025-10-30&granularity=Monthly"
```

### Azure Test 5: GET request (Specific Subscription)
```bash
curl "http://localhost:8000/azure/cost/export?subscription_id=12345678-1234-1234-1234-123456789abc&start_date=2025-08-01&end_date=2025-10-30&granularity=Daily"
```

---

## 📊 **Step 6: Verify Response Format**

All successful responses should have this structure:

```json
{
  "success": true,
  "message": "Cost data exported successfully",
  "total_records": <number>,
  "cost_data": [
    {
      "TIME_PERIOD": {"Start": "...", "End": "..."},
      "ID": "...",
      "GROUPBY_FILTER": "...",
      "COST": "... USD"
    }
  ],
  "request_parameters": {
    "start_date": "...",
    "end_date": "...",
    "granularity": "..."
  }
}
```

---

## 🔧 **Step 7: Test Error Handling**

### Test 1: Invalid Date Format
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "invalid-date",
    "end_date": "2025-10-30"
  }'
```

### Test 2: Azure SDK Not Available
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30"
  }'
```
*Expected if Azure SDK not installed: 503 Service Unavailable*

### Test 3: Invalid AWS Profile
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "non-existent-profile",
    "start_date": "2025-08-01",
    "end_date": "2025-10-30"
  }'
```

### Test 4: Invalid Azure Subscription ID
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription_id": "invalid-subscription-id",
    "start_date": "2025-08-01",
    "end_date": "2025-10-30"
  }'
```

---

## 🏃‍♂️ **Step 8: Automated Test Script**

Create this comprehensive test script:

```bash
#!/bin/bash
# comprehensive_test.sh

echo "🧪 Testing eraXplor API Comprehensively..."
BASE_URL="http://localhost:8000"

echo "✅ 1. Testing root endpoint..."
curl -s "$BASE_URL/" | jq '.'

echo "✅ 2. Testing AWS endpoint (default parameters)..."
curl -s -X POST "$BASE_URL/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.request_parameters'

echo "✅ 3. Testing AWS endpoint (custom parameters)..."
curl -s -X POST "$BASE_URL/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "MONTHLY",
    "group_by": "SERVICE"
  }' | jq '.total_records'

echo "✅ 4. Testing Azure endpoint (all subscriptions)..."
curl -s -X POST "$BASE_URL/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "Monthly"
  }' | jq '.request_parameters'

echo "✅ 5. Testing GET requests..."
curl -s "$BASE_URL/aws/cost/export?granularity=DAILY" | jq '.message'

echo "🎉 All tests completed!"
```

Make it executable and run:
```bash
chmod +x comprehensive_test.sh
./comprehensive_test.sh
```

---

## 📈 **Step 9: Monitor Server Logs**

While testing, watch the server terminal for:

### Expected Log Messages

**AWS Requests:**
```
Fetching AWS cost data from 2025-08-01 to 2025-10-30
Using profile: default, Group by: LINKED_ACCOUNT
Retrieved 31 cost records
INFO: 127.0.0.1:54321 - "POST /aws/cost/export HTTP/1.1" 200 OK
```

**Azure Requests (Specific Subscription):**
```
Fetching Azure cost data from 2025,08,01 to 2025,10,30
Subscription ID: 12345678-..., Granularity: Monthly
Retrieved 15 cost records
INFO: 127.0.0.1:54321 - "POST /azure/cost/export HTTP/1.1" 200 OK
```

**Azure Requests (All Subscriptions):**
```
Fetching Azure cost data from 2025,08,01 to 2025,10,30
No subscription ID provided - fetching all subscriptions, Granularity: Monthly
Retrieved 45 cost records
INFO: 127.0.0.1:54321 - "POST /azure/cost/export HTTP/1.1" 200 OK
```

### Error Log Examples

**AWS Profile Error:**
```
Error exporting AWS costs: The config profile (non-existent-profile) could not be found
INFO: 127.0.0.1:54321 - "POST /aws/cost/export HTTP/1.1" 500 Internal Server Error
```

**Azure SDK Missing:**
```
Azure module not available: No module named 'azure.identity'
Azure endpoints will return an error message
INFO: 127.0.0.1:54321 - "POST /azure/cost/export HTTP/1.1" 503 Service Unavailable
```

---

## 🎯 **Step 10: Expected Test Results**

### ✅ **Successful Tests Should Show:**

1. **HTTP Status Codes:**
   - 200 OK for successful requests
   - Appropriate error codes for failures

2. **Response Structure:**
   - `"success": true` for valid requests
   - `total_records` matching actual data count
   - Proper `cost_data` array with TIME_PERIOD, ID, GROUPBY_FILTER, COST
   - Correct `request_parameters` echo

3. **Data Validation:**
   - Date ranges respected
   - Granularity applied correctly
   - AWS group_by filters working
   - Azure subscription logic functioning

### ❌ **Common Issues to Check:**

1. **Authentication Problems:**
   - AWS credentials not configured → 500 error
   - Azure login expired → Azure API errors
   - Insufficient permissions → Access denied errors

2. **Module Availability:**
   - Azure SDK not installed → 503 Service Unavailable
   - Import errors → Module not found exceptions

3. **Parameter Validation:**
   - Invalid date formats → Parsing errors
   - Unsupported granularity values → Validation errors
   - Missing required Azure permissions → API errors

4. **Network & API Limits:**
   - AWS Cost Explorer API limits → Rate limiting errors
   - Azure Cost Management API limits → Quota exceeded errors
   - Network connectivity issues → Connection timeouts

---

## 🚀 **Step 11: Performance Testing**

### Load Testing (Optional)
```bash
# Install hey for load testing
go get -u github.com/rakyll/hey

# Test with 10 concurrent requests
hey -n 10 -c 2 -m POST \
  -H "Content-Type: application/json" \
  -d '{"granularity":"MONTHLY"}' \
  http://localhost:8000/aws/cost/export
```

### Response Time Monitoring
```bash
# Time a single request
time curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{"granularity":"MONTHLY"}'
```

---

## 🎉 **Your eraXplor API Testing is Complete!**

✅ **Basic Connectivity** - Root, docs, and health endpoints  
✅ **AWS Functionality** - All parameters, granularities, and group_by options  
✅ **Azure Functionality** - Both specific and all-subscriptions scenarios  
✅ **Error Handling** - Authentication, validation, and module availability  
✅ **Performance Validation** - Response times and concurrent requests  

Your API is production-ready! 🚀

## 🔧 **Step 6: Test Error Handling**

### Test Invalid Dates
```bash
curl -X POST "http://localhost:8000/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "invalid-date",
    "end_date": "2025-10-30"
  }'
```

### Test Missing Required Parameters (Azure)
```bash
curl -X POST "http://localhost:8000/azure/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30"
  }'
```

---

## 🏃‍♂️ **Quick Test Script**

Create this test script to run multiple tests:

```bash
#!/bin/bash
# test_api.sh

echo "🧪 Testing eraXplor API..."
BASE_URL="http://localhost:8000"

echo "✅ Testing root endpoint..."
curl -s "$BASE_URL/" | jq '.'

echo "✅ Testing AWS endpoint..."
curl -s -X POST "$BASE_URL/aws/cost/export" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-01",
    "end_date": "2025-10-30",
    "granularity": "MONTHLY"
  }' | jq '.request_parameters'

echo "✅ All tests completed!"
```

Make it executable and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📈 **Step 7: Monitor Server Logs**

While testing, watch the server terminal for:
- Request processing messages
- Cost data retrieval confirmations
- Error messages (if any)

Example log output:
```
Fetching AWS cost data from 2025-08-01 to 2025-10-30
Using profile: default, Group by: LINKED_ACCOUNT
Retrieved 31 cost records
INFO: 127.0.0.1:54321 - "POST /aws/cost/export HTTP/1.1" 200 OK
```

---

## 🎯 **Expected Test Results**

### ✅ **Successful Tests Should Show:**
- HTTP 200 status codes
- JSON responses with `"success": true`
- Proper data in `cost_data` array
- Correct `request_parameters` echo

### ❌ **Common Issues to Check:**
- AWS credentials not configured → 500 error
- Azure SDK not installed → Import error  
- Invalid date formats → Parsing errors
- Missing subscription permissions → Azure API errors

---

## 🚀 **Production Testing**

For production testing, consider:
1. **Load Testing**: Use tools like `hey` or `wrk`
2. **Integration Testing**: Test with real applications
3. **Performance Monitoring**: Check response times
4. **Error Rate Monitoring**: Track failed requests

Your eraXplor API is ready for comprehensive testing! 🎉