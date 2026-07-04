# test_final_state.py

import pytest
import requests
import datetime
import locale
import os
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

API_URL = "http://127.0.0.1:8080/time"
API_KEY = "9a8b7c6d5e4f3g2h"

def test_missing_api_key():
    """Test that requests without the API key return HTTP 401."""
    try:
        response = requests.get(API_URL, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {API_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing API key, got {response.status_code}"

def test_invalid_api_key():
    """Test that requests with an invalid API key return HTTP 401."""
    headers = {"X-API-Key": "invalid_key_123"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {API_URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid API key, got {response.status_code}"

def test_valid_api_key_and_response_format():
    """Test that requests with the valid API key return HTTP 200 and correctly formatted time."""
    headers = {"X-API-Key": API_KEY}
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to proxy at {API_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid API key, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "current_time" in data, "JSON response missing 'current_time' key"

    current_time_str = data["current_time"]

    # Check for French locale indicators (days or months)
    french_days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    french_months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

    lower_time_str = current_time_str.lower()
    has_french_day = any(day in lower_time_str for day in french_days)
    has_french_month = any(month in lower_time_str for month in french_months)

    assert has_french_day, f"Expected French day in current_time string, got: {current_time_str}"
    assert has_french_month, f"Expected French month in current_time string, got: {current_time_str}"

    # Check for Europe/Paris timezone abbreviations (CET or CEST)
    assert "CET" in current_time_str or "CEST" in current_time_str, f"Expected Europe/Paris timezone (CET/CEST) in current_time string, got: {current_time_str}"