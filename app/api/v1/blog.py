from typing import List
from fastapi import APIRouter, HTTPException, Request
from app.schemas.responses import ApiResponse
from app.schemas.blog import (
    BlogViewResponse,
    BlogAnalyticsResponse,
    BlogMultipleAnalyticsRequest,
    BlogMultipleAnalyticsResponse,
    BlogStatsResponse
)
from app.services.blog_service import blog_service

router = APIRouter()


@router.post("/blog/analytics/{slug}/view", response_model=ApiResponse[BlogViewResponse])
async def increment_blog_view(slug: str, request: Request):
    """Increment blog view count (simplified endpoint)."""
    try:
        # Extract headers
        session_id = request.headers.get("X-Session-ID")
        user_agent = request.headers.get("X-User-Agent")
        referrer = request.headers.get("X-Referrer")

        result = await blog_service.increment_blog_view(
            slug=slug,
            session_id=session_id,
            user_agent=user_agent,
            referrer=referrer
        )

        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blog/analytics/{slug}", response_model=ApiResponse[BlogAnalyticsResponse])
async def get_blog_analytics(slug: str):
    """Get analytics for specific blog post."""
    try:
        result = await blog_service.get_blog_analytics(slug)
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/blog/analytics/multiple", response_model=ApiResponse[List[BlogMultipleAnalyticsResponse]])
async def get_multiple_blog_analytics(request: BlogMultipleAnalyticsRequest):
    """Get analytics for multiple blog posts."""
    try:
        result = await blog_service.get_multiple_blog_analytics(request.slugs)
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blog/analytics/stats", response_model=ApiResponse[BlogStatsResponse])
async def get_blog_stats():
    """Get overall blog analytics."""
    try:
        result = await blog_service.get_blog_stats()
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blog/views/{slug}", response_model=ApiResponse[BlogAnalyticsResponse])
async def get_blog_views(slug: str):
    """Get view count for specific blog post (alias for analytics endpoint)."""
    try:
        result = await blog_service.get_blog_analytics(slug)
        return ApiResponse(
            success=True,
            data={"data": result}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blog/views", response_model=ApiResponse[List[BlogMultipleAnalyticsResponse]])
async def get_multiple_blog_views(slugs: str):
    """Get view counts for multiple blog posts (alias for analytics endpoint)."""
    try:
        slug_list = [s.strip() for s in slugs.split(',') if s.strip()]
        result = await blog_service.get_multiple_blog_analytics(slug_list)
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))