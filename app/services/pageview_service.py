from typing import List, Dict
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from ..schemas.pageviews import (
    PageviewRequest,
    PageviewResponse,
    PageviewStatsResponse
)


class MemoryPageviewService:
    """In-memory pageview tracking service for development."""

    def __init__(self):
        # In-memory storage (will be replaced with database)
        self.pageviews: List[dict] = []

    async def track_pageview(
        self,
        request: PageviewRequest,
        screen_resolution: str = None,
        timezone_str: str = None,
        platform: str = None,
        session_id: str = None
    ) -> PageviewResponse:
        """Track a page view."""
        pageview_id = str(uuid4())
        now = datetime.now(timezone.utc)

        pageview = {
            "id": pageview_id,
            "url": request.url,
            "title": request.title,
            "referrer": request.referrer,
            "user_agent": request.user_agent,
            "timestamp": request.timestamp or now,
            "tracked_at": now,
            "screen_resolution": screen_resolution,
            "timezone": timezone_str,
            "platform": platform,
            "session_id": session_id
        }

        self.pageviews.append(pageview)

        return PageviewResponse(
            pageview_id=pageview_id,
            tracked_at=now
        )

    async def get_pageview_stats(self) -> PageviewStatsResponse:
        """Get pageview statistics."""
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        week_start = today_start - timedelta(days=7)

        # Filter pageviews by time periods
        total_pageviews = len(self.pageviews)
        today_pageviews = len([p for p in self.pageviews if p["timestamp"] >= today_start])
        yesterday_pageviews = len([p for p in self.pageviews if yesterday_start <= p["timestamp"] < today_start])
        week_pageviews = len([p for p in self.pageviews if p["timestamp"] >= week_start])

        # Unique URLs
        unique_urls = len(set(p["url"] for p in self.pageviews))

        # Top pages
        url_counts = {}
        for pageview in self.pageviews:
            url = pageview["url"]
            if url not in url_counts:
                url_counts[url] = {"count": 0, "title": pageview.get("title", url)}
            url_counts[url]["count"] += 1

        top_pages = [
            {"url": url, "count": data["count"], "title": data["title"]}
            for url, data in sorted(url_counts.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
        ]

        return PageviewStatsResponse(
            total=total_pageviews,
            today=today_pageviews,
            yesterday=yesterday_pageviews,
            this_week=week_pageviews,
            unique_urls=unique_urls,
            top_pages=top_pages
        )


# Global service instance
pageview_service = MemoryPageviewService()