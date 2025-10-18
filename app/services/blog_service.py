from typing import List, Dict, Optional
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from ..schemas.blog import (
    BlogViewResponse,
    BlogAnalyticsResponse,
    BlogMultipleAnalyticsResponse,
    BlogStatsResponse
)
from ..services.visitor_service import visitor_service


class MemoryBlogService:
    """In-memory blog analytics service for development."""

    def __init__(self):
        # This will use the visitor service's blog views data
        pass

    async def increment_blog_view(
        self,
        slug: str,
        session_id: str = None,
        user_agent: str = None,
        referrer: str = None
    ) -> BlogViewResponse:
        """Increment blog view count (simplified endpoint)."""
        # For now, we'll create a simple visitor if no session_id is provided
        if not session_id:
            # This is a simplified approach - in production, we'd have proper session management
            pass

        # Get current views for this blog
        current_data = await visitor_service.get_blog_views(slug)

        # Create a simple blog view entry through visitor service
        # In a real implementation, this would be more sophisticated
        visitor_id = "anonymous"  # Simplified for now

        from ..schemas.visitors import VisitorBlogViewRequest
        view_request = VisitorBlogViewRequest(
            visitor_id=visitor_id,
            blog_slug=slug,
            blog_title=f"Blog post: {slug}"  # Simplified
        )

        view_result = await visitor_service.track_blog_view(view_request)

        # Get updated stats
        updated_data = await visitor_service.get_blog_views(slug)

        return BlogViewResponse(
            slug=slug,
            total_views=updated_data.total_views,
            unique_views=updated_data.unique_views,
            is_new_view=view_result.is_new_view
        )

    async def get_blog_analytics(self, slug: str) -> BlogAnalyticsResponse:
        """Get analytics for specific blog post."""
        views_data = await visitor_service.get_blog_views(slug)

        # Generate some sample daily views data
        daily_views = []
        now = datetime.now(timezone.utc)
        for i in range(30):  # Last 30 days
            date = (now - timedelta(days=i)).date()
            # Simplified: just use some sample data
            daily_views.append({
                "date": date.isoformat(),
                "views": max(0, views_data.total_views - i * 2),
                "uniqueViews": max(0, views_data.unique_views - i)
            })

        return BlogAnalyticsResponse(
            slug=slug,
            total_views=views_data.total_views,
            unique_views=views_data.unique_views,
            recent_views=views_data.recent_views,
            last_viewed_at=views_data.last_viewed_at,
            daily_views=list(reversed(daily_views))  # Most recent first
        )

    async def get_multiple_blog_analytics(self, slugs: List[str]) -> List[BlogMultipleAnalyticsResponse]:
        """Get analytics for multiple blog posts."""
        results = []
        for slug in slugs:
            views_data = await visitor_service.get_blog_views(slug)
            results.append(BlogMultipleAnalyticsResponse(
                slug=slug,
                total_views=views_data.total_views,
                unique_views=views_data.unique_views,
                recent_views=views_data.recent_views
            ))
        return results

    async def get_blog_stats(self) -> BlogStatsResponse:
        """Get overall blog analytics."""
        visitor_stats = await visitor_service.get_visitor_stats()

        # Calculate stats
        total_views = visitor_stats.total_blog_views
        unique_views = visitor_stats.unique_blog_views

        # Count unique blog posts
        unique_slugs = set()
        for view in visitor_service.blog_views:
            unique_slugs.add(view["blog_slug"])
        total_blog_posts = len(unique_slugs)

        # Calculate average
        average_views = total_views / total_blog_posts if total_blog_posts > 0 else 0

        # Get top posts
        top_posts = visitor_stats.top_blog_posts

        return BlogStatsResponse(
            total_blog_posts=total_blog_posts,
            total_views=total_views,
            total_unique_views=unique_views,
            average_views_per_post=average_views,
            top_posts=top_posts
        )


# Global service instance
blog_service = MemoryBlogService()