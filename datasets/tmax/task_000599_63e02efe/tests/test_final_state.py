# test_final_state.py
import time
import requests
import pytest

API_URL = "http://127.0.0.1:8080/top-words"
VALID_TOKEN = "SecretAutomationToken2024"

def test_unauthorized_no_token():
    """Test that omitting the Bearer token results in a 401 response."""
    try:
        response = requests.get(API_URL, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for no token, got {response.status_code}"

def test_unauthorized_bad_token():
    """Test that a bad Bearer token results in a 401 response."""
    headers = {"Authorization": "Bearer BadToken123"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for bad token, got {response.status_code}"

def test_authorized_success():
    """Test that the correct Bearer token returns the top words JSON."""
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    # The processor takes up to 10 seconds to generate the first window.
    # We will poll for up to 15 seconds.
    max_retries = 15
    for i in range(max_retries):
        try:
            response = requests.get(API_URL, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "top_words" in data and isinstance(data["top_words"], list) and len(data["top_words"]) > 0:
                    break
        except requests.RequestException:
            pass
        time.sleep(1)
    else:
        # Final attempt to get the exact failure reason
        try:
            response = requests.get(API_URL, headers=headers, timeout=5)
            assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"
            data = response.json()
            assert "top_words" in data, "Response JSON missing 'top_words' key."
            assert isinstance(data["top_words"], list), "'top_words' must be a list."
            assert len(data["top_words"]) == 5, f"Expected 5 top words, got {len(data['top_words'])}. Words: {data['top_words']}"
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to API: {e}")

    # If we broke out of the loop successfully, we still assert the conditions to ensure correctness
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert "top_words" in data, "Response JSON missing 'top_words' key."
    assert isinstance(data["top_words"], list), "'top_words' must be a list."
    assert len(data["top_words"]) <= 5, f"Expected up to 5 top words, got {len(data['top_words'])}."
    for word in data["top_words"]:
        assert isinstance(word, str), "Each top word must be a string."