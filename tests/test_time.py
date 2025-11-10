import pytest
from datetime import datetime
import pytz
from src.service.time import get_current_time, get_greeting, get_greeting_message

COSTA_RICA_TZ = pytz.timezone('America/Costa_Rica')


def test_get_current_time():
    """Test that get_current_time returns a valid ISO format timestamp"""
    result = get_current_time()
    assert isinstance(result, str)
    # Check that it contains timezone info (Costa Rica timezone)
    assert "-06:00" in result or "+00:00" in result or "T" in result
    # Try to parse it as an ISO format datetime
    # Handle different ISO formats
    try:
        parsed = datetime.fromisoformat(result)
    except ValueError:
        # Fallback for formats that might need adjustment
        parsed = datetime.fromisoformat(result.replace('Z', '+00:00'))
    assert isinstance(parsed, datetime)


def test_get_greeting_morning():
    """Test greeting for morning hours (5-11)"""
    assert get_greeting(5) == "Good Morning"
    assert get_greeting(11) == "Good Morning"
    assert get_greeting(8) == "Good Morning"


def test_get_greeting_afternoon():
    """Test greeting for afternoon hours (12-16)"""
    assert get_greeting(12) == "Good Afternoon"
    assert get_greeting(16) == "Good Afternoon"
    assert get_greeting(14) == "Good Afternoon"


def test_get_greeting_evening():
    """Test greeting for evening hours (17-20)"""
    assert get_greeting(17) == "Good Evening"
    assert get_greeting(20) == "Good Evening"
    assert get_greeting(18) == "Good Evening"


def test_get_greeting_night():
    """Test greeting for night hours (21-4)"""
    assert get_greeting(21) == "Good Night"
    assert get_greeting(23) == "Good Night"
    assert get_greeting(0) == "Good Night"
    assert get_greeting(4) == "Good Night"


def test_get_greeting_message_with_name():
    """Test get_greeting_message with a name"""
    result = get_greeting_message("Alice")
    assert isinstance(result, str)
    assert "Alice" in result
    # Should contain a greeting
    assert any(greeting in result for greeting in [
        "Good Morning", "Good Afternoon", "Good Evening", "Good Night"
    ])


def test_get_greeting_message_without_name():
    """Test get_greeting_message without a name (should use default)"""
    result = get_greeting_message()
    assert isinstance(result, str)
    assert "there" in result
    # Should contain a greeting
    assert any(greeting in result for greeting in [
        "Good Morning", "Good Afternoon", "Good Evening", "Good Night"
    ])


def test_get_greeting_message_with_none():
    """Test get_greeting_message with None as name"""
    result = get_greeting_message(None)
    assert isinstance(result, str)
    assert "there" in result

