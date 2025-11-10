import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_healthz_endpoint():
    """Test the health check endpoint"""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_now_endpoint():
    """Test the /now endpoint returns a valid ISO timestamp"""
    response = client.get("/now")
    assert response.status_code == 200
    assert "now" in response.json()
    # Check that the response contains a valid ISO format timestamp
    now_value = response.json()["now"]
    assert isinstance(now_value, str)
    assert "T" in now_value or "-" in now_value  # Basic ISO format check


def test_hello_endpoint_without_name():
    """Test the /hello endpoint without a name parameter"""
    response = client.get("/hello")
    assert response.status_code == 200
    assert "message" in response.json()
    message = response.json()["message"]
    assert isinstance(message, str)
    assert "there" in message  # Default name should be "there"


def test_hello_endpoint_with_name():
    """Test the /hello endpoint with a name parameter"""
    response = client.get("/hello?name=TestUser")
    assert response.status_code == 200
    assert "message" in response.json()
    message = response.json()["message"]
    assert isinstance(message, str)
    assert "TestUser" in message


def test_hello_endpoint_greeting_format():
    """Test that greeting messages follow the expected format"""
    response = client.get("/hello?name=Alice")
    assert response.status_code == 200
    message = response.json()["message"]
    # Should contain a greeting (Good Morning/Afternoon/Evening/Night) and the name
    assert any(greeting in message for greeting in [
        "Good Morning", "Good Afternoon", "Good Evening", "Good Night"
    ])
    assert "Alice" in message


def test_api_docs_endpoint():
    """Test that the API documentation endpoint is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema_endpoint():
    """Test that the OpenAPI schema endpoint is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
    assert "info" in response.json()

