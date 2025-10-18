from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class VisitorTrackRequest(BaseModel):
    """Request payload for tracking visitors."""
    visitor_id: Optional[str] = Field(None, description="Optional existing visitor ID")
    user_agent: str = Field(..., description="Visitor's user agent string")
    accept_language: str = Field(..., description="Visitor's accepted languages")
    screen_resolution: str = Field(..., description="Visitor's screen resolution")
    timezone: str = Field(..., description="Visitor's timezone")
    platform: str = Field(..., description="Visitor's platform/OS")
    language: str = Field(..., description="Visitor's language")
    referrer: Optional[str] = Field(None, description="Visitor's referrer")


class VisitorTrackResponse(BaseModel):
    """Response payload for visitor tracking."""
    visitor_id: str = Field(..., description="Unique visitor identifier")
    is_new_visitor: bool = Field(..., description="Whether this is a new visitor")
    total_visits: int = Field(..., description="Total number of visits")
    last_visit_at: datetime = Field(..., description="Timestamp of last visit")


class VisitorBlogViewRequest(BaseModel):
    """Request payload for tracking blog views."""
    visitor_id: str = Field(..., description="Visitor ID")
    blog_slug: str = Field(..., description="Blog post slug")
    blog_title: str = Field(..., description="Blog post title")


class VisitorBlogViewResponse(BaseModel):
    """Response payload for blog view tracking."""
    view_id: str = Field(..., description="Unique view identifier")
    is_new_view: bool = Field(..., description="Whether this is a new view")
    total_blog_views: int = Field(..., description="Total blog views")


class VisitorStatsResponse(BaseModel):
    """Response payload for visitor statistics."""
    total_visitors: int = Field(..., description="Total unique visitors")
    new_visitors: int = Field(..., description="Number of new visitors")
    returning_visitors: int = Field(..., description="Number of returning visitors")
    total_blog_views: int = Field(..., description="Total blog views")
    unique_blog_views: int = Field(..., description="Unique blog views")
    top_blog_posts: list[dict] = Field(..., description="Top blog posts")
    recent_visitors: list[dict] = Field(..., description="Recent visitors")


class VisitorBlogViewsResponse(BaseModel):
    """Response payload for specific blog post views."""
    slug: str = Field(..., description="Blog post slug")
    total_views: int = Field(..., description="Total views")
    unique_views: int = Field(..., description="Unique views")
    recent_views: int = Field(..., description="Recent views")
    last_viewed_at: Optional[datetime] = Field(None, description="Last view timestamp")