from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings
from app.schemas.health import HealthResponse, HealthData

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""

    health_data = HealthData(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        environment=settings.ENVIRONMENT
    )

    return HealthResponse(
        success=True,
        data=health_data.dict()
    )


@router.get("/health/detailed", response_model=HealthResponse)
async def detailed_health_check():
    """Detailed health check with database status."""

    # TODO: Add database connectivity check
    # TODO: Add external service checks

    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "features": {
            "analytics": settings.ENABLE_ANALYTICS,
            "feedback": settings.ENABLE_FEEDBACK,
            "production_only_views": settings.INCREMENT_VIEWS_ONLY_IN_PRODUCTION
        }
    }

    return HealthResponse(
        success=True,
        data=health_data
    )