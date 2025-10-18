from pydantic import BaseModel, Field
from typing import Optional, Any, Generic, TypeVar
from datetime import datetime

DataType = TypeVar('DataType')


class ApiResponse(BaseModel, Generic[DataType]):
    """Standard API response format."""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[DataType] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if success is false")
    message: Optional[str] = Field(None, description="Optional message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class ApiError(BaseModel):
    """Standard API error format."""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    details: Optional[Any] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


# Common response types
class SuccessResponse(ApiResponse[dict]):
    """Success response with data."""
    pass


class EmptySuccessResponse(ApiResponse[None]):
    """Success response with no data."""
    pass


# Health check specific responses
class HealthData(BaseModel):
    """Health check data."""
    status: str
    timestamp: datetime
    version: str
    environment: str


class HealthResponse(ApiResponse[HealthData]):
    """Health check response."""
    pass