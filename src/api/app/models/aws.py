"""AWS cost management data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel  # Pylint: disable=import-error


class AWSCostRequest(BaseModel):  # Pylint: disable=too-few-public-methods
    """Request model for AWS cost export."""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    profile: str = "default"
    group_by: str = "LINKED_ACCOUNT"
    granularity: str = "MONTHLY"


class AWSCostResponse(BaseModel):  # Pylint: disable=too-few-public-methods
    """Response model for AWS cost export."""
    success: bool
    message: str
    total_records: int
    cost_data: List[Dict[str, Any]]
    request_parameters: Dict[str, str]
