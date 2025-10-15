from pydantic import BaseModel, ConfigDict
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response."""
    success: bool
    data: dict


class HealthData(BaseModel):
    """Health check data."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    status: str
    timestamp: datetime
    version: str
    environment: str
