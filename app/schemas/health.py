from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response."""
    success: bool
    data: dict


class HealthData(BaseModel):
    """Health check data."""
    status: str
    timestamp: datetime
    version: str
    environment: str