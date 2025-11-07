"""Application configuration settings."""

import os
from typing import List


class Settings:
    """Application settings configuration."""
    
    # Project Information
    PROJECT_NAME: str = "eraXplor API"
    PROJECT_DESCRIPTION: str = "A RESTful API for AWS and Azure cost data export"
    API_VERSION: str = "1.0.0"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    
    # AWS Configuration (Optional - can be overridden by request parameters)
    AWS_DEFAULT_PROFILE: str = "default"
    AWS_DEFAULT_REGION: str = "us-east-1"
    
    # Azure Configuration (Optional - can be overridden by request parameters)
    AZURE_DEFAULT_SUBSCRIPTION_ID: str = ""
    
    # File Export Configuration
    MAX_CSV_ROWS: int = 10000
    EXPORT_TEMP_DIR: str = "/tmp/eraxplor_exports"
    
    # Request Limits
    MAX_DATE_RANGE_MONTHS: int = 14  # AWS limitation
    REQUEST_TIMEOUT_SECONDS: int = 300  # 5 minutes


# Create settings instance
settings = Settings()