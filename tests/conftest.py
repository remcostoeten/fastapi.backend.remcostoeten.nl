import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
# from app.core.database import db  # TODO: uncomment when database is implemented


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Setup database for tests."""
    # TODO: Set up test database when implemented
    # For now, we'll skip database operations
    yield
    # TODO: Cleanup test database when implemented


@pytest.fixture
def sample_health_response():
    """Sample health response for testing."""
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00.000000",
            "version": "1.0.0",
            "environment": "test"
        }
    }