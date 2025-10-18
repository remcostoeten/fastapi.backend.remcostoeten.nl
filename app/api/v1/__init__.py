# API v1 routes
from .health import router as health_router
from .visitors import router as visitors_router
from .pageviews import router as pageviews_router
from .blog import router as blog_router

__all__ = ["health_router", "visitors_router", "pageviews_router", "blog_router"]
