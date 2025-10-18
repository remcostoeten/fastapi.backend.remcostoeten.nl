import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["status"] == "healthy"
    assert "timestamp" in data["data"]
    assert data["data"]["version"] == "1.0.0"


def test_detailed_health_check():
    """Test the detailed health check endpoint."""
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["status"] == "healthy"
    assert "features" in data["data"]


def test_visitor_track():
    """Test the visitor tracking endpoint."""
    visitor_data = {
        "user_agent": "Mozilla/5.0 (Test Browser)",
        "accept_language": "en-US,en;q=0.9",
        "screen_resolution": "1920x1080",
        "timezone": "America/New_York",
        "platform": "Web",
        "language": "en",
        "referrer": "https://google.com"
    }

    response = client.post("/api/v1/visitors/track", json=visitor_data)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "visitor_id" in data["data"]
    assert "is_new_visitor" in data["data"]
    assert "total_visits" in data["data"]


def test_pageview_track():
    """Test the pageview tracking endpoint."""
    pageview_data = {
        "url": "https://example.com/test-page",
        "title": "Test Page",
        "referrer": "https://google.com"
    }

    headers = {
        "X-Screen-Resolution": "1920x1080",
        "X-Timezone": "America/New_York",
        "X-Platform": "Web",
        "X-Session-ID": "test-session-123"
    }

    response = client.post("/api/v1/pageviews", json=pageview_data, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "pageview_id" in data["data"]
    assert "tracked_at" in data["data"]


def test_blog_analytics_increment():
    """Test the blog analytics increment endpoint."""
    headers = {
        "X-Session-ID": "test-session-123",
        "X-User-Agent": "Mozilla/5.0 (Test Browser)",
        "X-Referrer": "https://google.com"
    }

    response = client.post("/api/v1/blog/analytics/test-blog-post/view", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["slug"] == "test-blog-post"
    assert "total_views" in data["data"]
    assert "unique_views" in data["data"]


def test_blog_analytics_get():
    """Test the blog analytics get endpoint."""
    response = client.get("/api/v1/blog/analytics/test-blog-post")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["slug"] == "test-blog-post"
    assert "total_views" in data["data"]
    assert "unique_views" in data["data"]


def test_pageview_stats():
    """Test the pageview statistics endpoint."""
    response = client.get("/api/v1/pageviews/stats")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "total" in data["data"]
    assert "today" in data["data"]
    assert "unique_urls" in data["data"]


def test_visitor_stats():
    """Test the visitor statistics endpoint."""
    response = client.get("/api/v1/visitors/stats")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "total_visitors" in data["data"]
    assert "total_blog_views" in data["data"]