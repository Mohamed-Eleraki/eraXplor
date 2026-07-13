"""AWS FOCUS workflow data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel  # Pylint: disable=import-error


class AWSFocusRequest(BaseModel):  # Pylint: disable=too-few-public-methods
    """Request model for AWS FOCUS workflow."""
    command: str = "configure"
    profile: str = "default"
    region: str = "us-east-1"
    stack_name: str = "CID-DataExports-Source"
    granularity: str = "MONTHLY"


class AWSFocusResponse(BaseModel):  # Pylint: disable=too-few-public-methods
    """Response model for AWS FOCUS workflow."""
    success: bool
    command: str
    message: str
    result: Optional[Dict[str, Any]] = None
    total_files: Optional[int] = None
    files: Optional[List[str]] = None
