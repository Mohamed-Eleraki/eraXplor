"""Azure cost management data models."""

from typing import Optional, List, Dict, Any


# Azure cost request structure (without Pydantic for simplicity)
class AzureCostRequestStructure:
    """Structure documentation for Azure cost export request."""
    subscription_id: Optional[str] = None  # Azure subscription ID
    start_date: Optional[str] = None       # YYYY-MM-DD format
    end_date: Optional[str] = None         # YYYY-MM-DD format
    granularity: str = "Monthly"           # Monthly or Daily


# Azure cost response structure (without Pydantic for simplicity)
class AzureCostResponseStructure:
    """Structure documentation for Azure cost export response."""
    success: bool
    message: str
    total_records: int
    cost_data: List[Dict[str, Any]]
    request_parameters: Dict[str, str]