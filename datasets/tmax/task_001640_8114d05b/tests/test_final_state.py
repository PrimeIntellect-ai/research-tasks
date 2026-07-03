# test_final_state.py

import os
import re
import requests
import pytest

def test_files_exist():
    assert os.path.isfile("/home/user/deploy.sh"), "/home/user/deploy.sh is missing"
    assert os.path.isfile("/home/user/edge_daemon.c"), "/home/user/edge_daemon.c is missing"
    assert os.path.isfile("/home/user/edge_daemon"), "/home/user/edge_daemon executable is missing"

def test_health_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check for Japanese characters or JST to verify locale/timezone
    body = response.text
    has_jp_chars = any(char in body for char in ['年', '月', '日', '時', '分', '秒', 'JST'])
    assert has_jp_chars, f"Response body does not appear to be formatted with ja_JP.UTF-8 locale and Asia/Tokyo timezone. Body: {body}"

def test_metrics_endpoint():
    try:
        response = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /metrics endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    body = response.text.strip()
    match = re.search(r'black_frames:\s*(\d+)', body)
    assert match is not None, f"Response body does not match expected format 'black_frames: <COUNT>'. Body: {body}"

    count = int(match.group(1))
    assert count == 42, f"Expected 42 black frames, got {count}"