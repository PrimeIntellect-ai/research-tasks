# test_final_state.py

import pytest
import requests
import json
import time

URL = "http://127.0.0.1:8080/"

def wait_for_server():
    for _ in range(10):
        try:
            requests.get(URL, timeout=1)
            return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False

def test_server_running():
    # We just need it to accept connections; a GET might fail with 400 or something, but the connection should succeed
    try:
        requests.post(URL, data="", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not listening on 127.0.0.1:8080")

def test_payload_1():
    payload = (
        '{"id": "1", "text": "Hello", "max_chars": 10}\n'
        '{"id": "2", "text": "こんにちは", "max_chars": 3}\n'
        '{"id": "3", "text": "Hello \\uD83C\\uDF0E", "max_chars": 10}\n'
        '{"id": "4", "text": "café", "max_chars": 4}\n'
        '{"id": "5", "text": "a", "max_chars": 1}\n'
    )

    try:
        response = requests.post(URL, data=payload, timeout=5)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("valid_count") == 4, f"Expected valid_count=4, got {data.get('valid_count')}"
    assert data.get("invalid_count") == 1, f"Expected invalid_count=1, got {data.get('invalid_count')}"
    assert data.get("avg_valid_len") == 4.25, f"Expected avg_valid_len=4.25, got {data.get('avg_valid_len')}"
    assert data.get("rolling_avg_3") == 4.00, f"Expected rolling_avg_3=4.00, got {data.get('rolling_avg_3')}"

def test_payload_2():
    payload = (
        '{"id": "1", "text": "テスト", "max_chars": 5}\n'
        '{"id": "2", "text": "\\uD83D\\uDE00", "max_chars": 0}\n'
        '{"id": "3", "text": "a", "max_chars": 10}\n'
        '{"id": "4", "text": "b", "max_chars": 10}\n'
        '{"id": "5", "text": "c", "max_chars": 10}\n'
        '{"id": "6", "text": "d", "max_chars": 10}\n'
    )

    try:
        response = requests.post(URL, data=payload, timeout=5)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("valid_count") == 5, f"Expected valid_count=5, got {data.get('valid_count')}"
    assert data.get("invalid_count") == 1, f"Expected invalid_count=1, got {data.get('invalid_count')}"
    assert data.get("avg_valid_len") == 1.40, f"Expected avg_valid_len=1.40, got {data.get('avg_valid_len')}"
    assert data.get("rolling_avg_3") == 1.00, f"Expected rolling_avg_3=1.00, got {data.get('rolling_avg_3')}"