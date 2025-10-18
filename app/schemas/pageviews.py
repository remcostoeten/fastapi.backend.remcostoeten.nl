from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class PageviewRequest(BaseModel):
    """Request payload for pageview tracking."""
    url: str = Field(..., description="Page URL")
    title: Optional[str] = Field(None, description="Page title")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    user_agent: Optional[str] = Field(None, description="User agent string")
    timestamp: Optional[datetime] = Field(None, description="Request timestamp")


class PageviewResponse(BaseModel):
    """Response payload for pageview tracking."""
    pageview_id: str = Field(..., description="Unique pageview identifier")
    tracked_at: datetime = Field(..., description="When the pageview was tracked")


class PageviewStatsResponse(BaseModel):
    """Response payload for pageview statistics."""
    total: int = Field(..., description="Total pageviews")
    today: int = Field(..., description="Pageviews today")
    yesterday: int = Field(..., description="Pageviews yesterday")
    this_week: int = Field(..., description="Pageviews this week")
    unique_urls: int = Field(..., description="Number of unique URLs")
    top_pages: list[dict] = Field(..., description="Top pages by view count")