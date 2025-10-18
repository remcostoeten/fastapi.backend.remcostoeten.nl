from typing import Dict, List, Optional
from datetime import datetime, timezone
from uuid import uuid4
import hashlib

from ..schemas.visitors import (
    VisitorTrackRequest,
    VisitorTrackResponse,
    VisitorBlogViewRequest,
    VisitorBlogViewResponse,
    VisitorStatsResponse,
    VisitorBlogViewsResponse
)


class MemoryVisitorService:
    """In-memory visitor tracking service for development."""

    def __init__(self):
        # In-memory storage (will be replaced with database)
        self.visitors: Dict[str, dict] = {}
        self.blog_views: List[dict] = []
        self.visitor_sessions: Dict[str, List[datetime]] = {}

    def _generate_fingerprint(self, request: VisitorTrackRequest) -> str:
        """Generate a unique fingerprint for the visitor."""
        fingerprint_data = f"{request.user_agent}|{request.accept_language}|{request.screen_resolution}|{request.timezone}|{request.platform}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32]

    async def track_visitor(self, request: VisitorTrackRequest) -> VisitorTrackResponse:
        """Track a new or returning visitor."""
        fingerprint = self._generate_fingerprint(request)
        now = datetime.now(timezone.utc)

        # Check if we have an existing visitor with this fingerprint
        existing_visitor_id = None
        for visitor_id, visitor_data in self.visitors.items():
            if visitor_data.get("fingerprint") == fingerprint:
                existing_visitor_id = visitor_id
                break

        if existing_visitor_id:
            # Returning visitor
            visitor = self.visitors[existing_visitor_id]
            visitor["total_visits"] = (visitor.get("total_visits", 1) + 1)
            visitor["last_visit_at"] = now

            # Track session
            if existing_visitor_id not in self.visitor_sessions:
                self.visitor_sessions[existing_visitor_id] = []
            self.visitor_sessions[existing_visitor_id].append(now)

            return VisitorTrackResponse(
                visitor_id=existing_visitor_id,
                is_new_visitor=False,
                total_visits=visitor["total_visits"],
                last_visit_at=now
            )
        else:
            # New visitor
            visitor_id = str(uuid4())
            visitor = {
                "id": visitor_id,
                "fingerprint": fingerprint,
                "user_agent": request.user_agent,
                "accept_language": request.accept_language,
                "screen_resolution": request.screen_resolution,
                "timezone": request.timezone,
                "platform": request.platform,
                "language": request.language,
                "referrer": request.referrer,
                "first_visit_at": now,
                "last_visit_at": now,
                "total_visits": 1,
                "is_new_visitor": True
            }

            self.visitors[visitor_id] = visitor
            self.visitor_sessions[visitor_id] = [now]

            return VisitorTrackResponse(
                visitor_id=visitor_id,
                is_new_visitor=True,
                total_visits=1,
                last_visit_at=now
            )

    async def track_blog_view(self, request: VisitorBlogViewRequest, is_localhost: bool = False) -> VisitorBlogViewResponse:
        """Track a blog view by a visitor."""
        view_id = str(uuid4())
        now = datetime.now(timezone.utc)

        # Check if visitor exists
        if request.visitor_id not in self.visitors:
            # Create visitor if doesn't exist (fallback)
            await self.track_visitor(VisitorTrackRequest(
                user_agent="unknown",
                accept_language="unknown",
                screen_resolution="unknown",
                timezone="UTC",
                platform="unknown",
                language="unknown"
            ))

        # Count existing views for this blog
        existing_views = [v for v in self.blog_views if v["blog_slug"] == request.blog_slug]
        unique_viewers = set(v["visitor_id"] for v in existing_views)
        is_new_view = request.visitor_id not in unique_viewers

        # Add new view with localhost flag
        view = {
            "id": view_id,
            "visitor_id": request.visitor_id,
            "blog_slug": request.blog_slug,
            "blog_title": request.blog_title,
            "viewed_at": now,
            "is_unique_view": is_new_view,
            "is_localhost": is_localhost
        }
        self.blog_views.append(view)

        return VisitorBlogViewResponse(
            view_id=view_id,
            is_new_view=is_new_view,
            total_blog_views=len(existing_views) + 1
        )

    async def get_visitor_stats(self) -> VisitorStatsResponse:
        """Get visitor statistics."""
        total_visitors = len(self.visitors)
        new_visitors = len([v for v in self.visitors.values() if v.get("total_visits", 1) == 1])
        returning_visitors = total_visitors - new_visitors

        # Blog view stats
        blog_views_by_slug = {}
        for view in self.blog_views:
            slug = view["blog_slug"]
            if slug not in blog_views_by_slug:
                blog_views_by_slug[slug] = {"count": 0, "unique_viewers": set(), "title": view["blog_title"]}
            blog_views_by_slug[slug]["count"] += 1
            blog_views_by_slug[slug]["unique_viewers"].add(view["visitor_id"])

        # Top blog posts
        top_blog_posts = []
        for slug, data in sorted(blog_views_by_slug.items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
            top_blog_posts.append({
                "slug": slug,
                "title": data["title"],
                "view_count": data["count"],
                "unique_viewers": len(data["unique_viewers"])
            })

        # Recent visitors
        recent_visitors = []
        for visitor_id, visitor in sorted(self.visitors.items(), key=lambda x: x[1]["last_visit_at"], reverse=True)[:10]:
            recent_visitors.append({
                "visitorId": visitor_id,
                "isNewVisitor": visitor.get("total_visits", 1) == 1,
                "totalVisits": visitor.get("total_visits", 1),
                "lastVisitAt": visitor["last_visit_at"].isoformat()
            })

        return VisitorStatsResponse(
            total_visitors=total_visitors,
            new_visitors=new_visitors,
            returning_visitors=returning_visitors,
            total_blog_views=len(self.blog_views),
            unique_blog_views=sum(len(data["unique_viewers"]) for data in blog_views_by_slug.values()),
            top_blog_posts=top_blog_posts,
            recent_visitors=recent_visitors
        )

    async def get_blog_views(self, slug: str) -> VisitorBlogViewsResponse:
        """Get view count for a specific blog post."""
        blog_views = [v for v in self.blog_views if v["blog_slug"] == slug]
        unique_viewers = set(v["visitor_id"] for v in blog_views)
        recent_views = len([v for v in blog_views if (datetime.now(timezone.utc) - v["viewed_at"]).days <= 7])
        last_viewed_at = max(v["viewed_at"] for v in blog_views) if blog_views else None

        return VisitorBlogViewsResponse(
            slug=slug,
            total_views=len(blog_views),
            unique_views=len(unique_viewers),
            recent_views=recent_views,
            last_viewed_at=last_viewed_at
        )


# Global service instance
visitor_service = MemoryVisitorService()