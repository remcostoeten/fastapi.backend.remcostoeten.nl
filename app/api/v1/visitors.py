from fastapi import APIRouter, HTTPException
from app.schemas.responses import ApiResponse
from app.schemas.visitors import (
    VisitorTrackRequest,
    VisitorTrackResponse,
    VisitorBlogViewRequest,
    VisitorBlogViewResponse,
    VisitorStatsResponse,
    VisitorBlogViewsResponse
)
from app.services.visitor_service import visitor_service

router = APIRouter()


@router.post("/visitors/track", response_model=ApiResponse[VisitorTrackResponse])
async def track_visitor(request: VisitorTrackRequest):
    """Track a new or returning visitor."""
    try:
        result = await visitor_service.track_visitor(request)
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visitors/track-blog-view", response_model=ApiResponse[VisitorBlogViewResponse])
async def track_blog_view(request: VisitorBlogViewRequest):
    """Track when a visitor views a blog post."""
    try:
        result = await visitor_service.track_blog_view(request)
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visitors/stats", response_model=ApiResponse[VisitorStatsResponse])
async def get_visitor_stats():
    """Get visitor statistics for analytics dashboard."""
    try:
        result = await visitor_service.get_visitor_stats()
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visitors/blog/{slug}/views", response_model=ApiResponse[VisitorBlogViewsResponse])
async def get_blog_views(slug: str):
    """Get view count for a specific blog post."""
    try:
        result = await visitor_service.get_blog_views(slug)
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))