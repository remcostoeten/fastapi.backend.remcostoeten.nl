import pytest
from fastapi.testclient import TestClient


def test_health_check_basic(client: TestClient):
    """Test basic health check endpoint."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert data["data"]["status"] == "healthy"
    assert "timestamp" in data["data"]
    assert data["data"]["version"] == "1.0.0"
    assert data["data"]["environment"] in ["development", "test", "production"]


def test_health_check_detailed(client: TestClient):
    """Test detailed health check endpoint."""
    response = client.get("/api/v1/health/detailed")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert data["data"]["status"] == "healthy"
    assert "features" in data["data"]

    # Check feature flags
    features = data["data"]["features"]
    assert "analytics" in features
    assert "feedback" in features
    assert "production_only_views" in features
    assert isinstance(features["analytics"], bool)
    assert isinstance(features["feedback"], bool)
    assert isinstance(features["production_only_views"], bool)


def test_health_check_response_structure(client: TestClient):
    """Test that health check response has the correct structure."""
    response = client.get("/api/v1/health")
    data = response.json()

    # Required top-level fields
    assert "success" in data
    assert "data" in data
    assert isinstance(data["success"], bool)
    assert isinstance(data["data"], dict)

    # Required data fields
    required_fields = ["status", "timestamp", "version", "environment"]
    for field in required_fields:
        assert field in data["data"]

    # Status should be healthy
    assert data["data"]["status"] == "healthy"

    # Version should be a string
    assert isinstance(data["data"]["version"], str)

    # Environment should be a string
    assert isinstance(data["data"]["environment"], str)


def test_health_check_cors_headers(client: TestClient):
    """Test that CORS headers are properly set."""
    response = client.get("/api/v1/health", headers={"Origin": "https://remcostoeten.nl"})

    # Should have CORS headers when Origin is present
    assert "access-control-allow-origin" in response.headers