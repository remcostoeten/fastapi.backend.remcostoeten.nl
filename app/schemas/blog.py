from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BlogViewRequest(BaseModel):
    """Request for blog view tracking (simplified endpoint)."""
    pass  # Data comes from headers


class BlogViewResponse(BaseModel):
    """Response for blog view tracking."""
    slug: str = Field(..., description="Blog post slug")
    total_views: int = Field(..., description="Total views")
    unique_views: int = Field(..., description="Unique views")
    is_new_view: bool = Field(..., description="Whether this is a new view")


class BlogAnalyticsResponse(BaseModel):
    """Response for blog analytics."""
    slug: str = Field(..., description="Blog post slug")
    total_views: int = Field(..., description="Total views")
    unique_views: int = Field(..., description="Unique views")
    recent_views: int = Field(..., description="Recent views")
    last_viewed_at: Optional[datetime] = Field(None, description="Last view timestamp")
    daily_views: List[dict] = Field(default_factory=list, description="Daily view breakdown")


class BlogMultipleAnalyticsRequest(BaseModel):
    """Request for multiple blog analytics."""
    slugs: List[str] = Field(..., description="List of blog slugs")


class BlogMultipleAnalyticsResponse(BaseModel):
    """Response for multiple blog analytics."""
    slug: str = Field(..., description="Blog post slug")
    total_views: int = Field(..., description="Total views")
    unique_views: int = Field(..., description="Unique views")
    recent_views: int = Field(..., description="Recent views")


class BlogStatsResponse(BaseModel):
    """Response for overall blog analytics."""
    total_blog_posts: int = Field(..., description="Total blog posts")
    total_views: int = Field(..., description="Total views across all posts")
    total_unique_views: int = Field(..., description="Total unique views")
    average_views_per_post: float = Field(..., description="Average views per post")
    top_posts: List[dict] = Field(..., description="Top performing posts")