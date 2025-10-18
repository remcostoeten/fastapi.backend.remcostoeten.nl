from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
# from .core.database import connect_to_database, disconnect_from_database
from .api.v1 import health_router, visitors_router, pageviews_router, blog_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    print(f"🚀 Starting API in {settings.ENVIRONMENT} mode")

    # TODO: Connect to database when implemented
    # if settings.ENABLE_ANALYTICS:
    #     await connect_to_database()

    yield

    # Shutdown
    print("🛑 Shutting down API")
    # TODO: Disconnect from database when implemented
    # if settings.ENABLE_ANALYTICS:
    #     await disconnect_from_database()


# Create FastAPI app
app = FastAPI(
    title="Remco Stoeten API",
    description="Simple, composable API for blog analytics and visitor tracking",
    version="1.0.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(visitors_router, prefix="/api/v1", tags=["Visitors"])
app.include_router(pageviews_router, prefix="/api/v1", tags=["Pageviews"])
app.include_router(blog_router, prefix="/api/v1", tags=["Blog"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Remco Stoeten API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.is_development else "disabled in production"
    }


@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "name": "Remco Stoeten API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "features": {
            "analytics": settings.ENABLE_ANALYTICS,
            "feedback": settings.ENABLE_FEEDBACK,
            "production_only_views": settings.INCREMENT_VIEWS_ONLY_IN_PRODUCTION
        },
        "endpoints": {
            "health": "/api/v1/health",
            "docs": "/docs" if settings.is_development else "disabled"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.is_development,
        log_level="info"
    )
