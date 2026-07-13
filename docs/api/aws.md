# AWS FOCUS API

This section documents the AWS FOCUS workflow endpoints for the eraXplor API.

---

## How to Run Locally

### Prerequisites

- Python 3.12+
- pip
- Git
- AWS CLI

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/Mohamed-Eleraki/eraXplor.git
cd eraXplor
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
cd src/api
pip install -r requirements.txt
```

4. **Configure AWS credentials:**
```bash
aws configure --profile default
# Or set credentials in ~/.aws/credentials
```

5. **Run the API server:**
```bash
cd src/api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

6. **Access the API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/

### Docker (Optional)

```bash
docker build -t eraxplor-api ./src/api
docker run -p 8000:8000 eraxplor-api
```

---

## API Information

- **API Name**: eraXplor API
- **Version**: 2.0.0
- **Base URL**: `http://localhost:8000`

---

## Root Endpoint

- **GET** `/` - Welcome message

---

## Interactive Documentation

- **GET** `/docs` - Swagger UI
- **GET** `/redoc` - ReDoc

---

## AWS FOCUS Endpoints

### POST `/aws/focus/run`

Run AWS FOCUS workflow using JSON request body.

**Request Body:**
```json
{
  "command": "configure",
  "profile": "default",
  "region": "us-east-1",
  "stack_name": "CID-DataExports-Source",
  "granularity": "MONTHLY"
}
```

**Parameters:**
- `command` (string, optional): `configure` or `download`. Default: `configure`
- `profile` (string, optional): AWS profile name. Default: "default"
- `region` (string, optional): AWS region. Default: "us-east-1"
- `stack_name` (string, optional): CloudFormation stack name. Default: "CID-DataExports-Source"
- `granularity` (string, optional): "HOURLY", "DAILY", or "MONTHLY" (used in `configure` mode)

---

### GET `/aws/focus/run`

Run AWS FOCUS workflow using query parameters.

**Query Parameters:**
- `command` (optional): `configure` or `download`
- `profile` (optional): AWS profile name
- `region` (optional): AWS region
- `stack_name` (optional): CloudFormation stack name
- `granularity` (optional): HOURLY/DAILY/MONTHLY (configure mode)

**Example:**
```bash
curl "http://localhost:8000/aws/focus/run?command=download&profile=default&region=us-east-1&stack_name=CID-DataExports-Source"
```

---

## Response Format

```json
{
  "success": true,
  "command": "download",
  "message": "AWS FOCUS parquet files downloaded successfully",
  "total_files": 2,
  "files": ["./downloaded_parquet_files/file1.parquet", "./downloaded_parquet_files/file2.parquet"]
}
```

---

## Error Responses

### General Error (500 Internal Server Error)
```json
{
  "error": true,
  "message": "Error running AWS FOCUS command: [detailed error message]"
}
```

---

## Testing AWS Endpoint

```bash
curl -X POST "http://localhost:8000/aws/focus/run" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "configure",
    "profile": "default",
    "region": "us-east-1",
    "stack_name": "CID-DataExports-Source",
    "granularity": "DAILY"
  }'
```

---

## Authentication Requirements

- AWS CLI configured with profiles
- Valid AWS credentials in `~/.aws/credentials`
- Appropriate IAM permissions for CloudFormation, S3, and FOCUS-related resources

---

## Dependencies

```
fastapi>=0.68.0
uvicorn>=0.15.0
boto3>=1.37.0
```

---

## Features

- AWS FOCUS stack configure command
- AWS FOCUS parquet download command
- Separate configure/download execution model
- Support for AWS profiles and regions

