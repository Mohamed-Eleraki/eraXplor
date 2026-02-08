# API Reference

This section provides auto-generated API reference documentation for the eraXplor API, extracted directly from the FastAPI application docstrings.

---

## 🚀 How to Run Locally

### Prerequisites

- Python 3.12+
- pip
- Git

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
cd api
pip install -r requirements.txt
```

4. **Configure credentials:**

**For AWS:**
```bash
aws configure --profile default
# Or set credentials in ~/.aws/credentials
```

**For Azure:**
```bash
az login
```

5. **Run the API server:**
```bash
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

6. **Access the API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/

### Docker (Optional)

```bash
docker build -t eraxplor-api ./api
docker run -p 8000:8000 eraxplor-api
```

---

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

