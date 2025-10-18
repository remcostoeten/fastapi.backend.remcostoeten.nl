from fastapi import APIRouter, HTTPException, Request
from app.schemas.responses import ApiResponse
from app.schemas.pageviews import (
    PageviewRequest,
    PageviewResponse,
    PageviewStatsResponse
)
from app.services.pageview_service import pageview_service

router = APIRouter()


@router.post("/pageviews", response_model=ApiResponse[PageviewResponse])
async def track_pageview(request: Request, pageview_request: PageviewRequest):
    """Track individual page views."""
    try:
        # Extract headers
        screen_resolution = request.headers.get("X-Screen-Resolution")
        timezone_str = request.headers.get("X-Timezone")
        platform = request.headers.get("X-Platform")
        session_id = request.headers.get("X-Session-ID")

        result = await pageview_service.track_pageview(
            request=pageview_request,
            screen_resolution=screen_resolution,
            timezone_str=timezone_str,
            platform=platform,
            session_id=session_id
        )

        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pageviews/stats", response_model=ApiResponse[PageviewStatsResponse])
async def get_pageview_stats():
    """Get pageview statistics."""
    try:
        result = await pageview_service.get_pageview_stats()
        return ApiResponse(
            success=True,
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))