"""Azure cost management data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel  # Pylint: disable=import-error


class AzureCostRequest(BaseModel):  # Pylint: disable=too-few-public-methods
    """Request model for Azure cost export."""
    start_date: Optional[str] = None        # YYYY-MM-DD format
    end_date: Optional[str] = None         # YYYY-MM-DD format
    granularity: str = "Monthly"           # Monthly or Daily
    group_by: str = "subscription"         # Group by dimension: subscription, ServiceName, ResourceGroupName


class AzureCostResponse(BaseModel):  # Pylint: disable=too-few-public-methods
    """Response model for Azure cost export."""
    success: bool
    message: str
    total_records: int
    cost_data: List[Dict[str, Any]]
    request_parameters: Dict[str, str]

