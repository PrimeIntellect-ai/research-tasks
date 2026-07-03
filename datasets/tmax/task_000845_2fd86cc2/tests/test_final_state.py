# test_final_state.py

import os
import requests
import pytest
import time

def test_system_config_not_overwritten():
    """Verify that the Zip Slip attack was mitigated and system_config.txt is intact."""
    config_path = "/app/system_config.txt"
    assert os.path.isfile(config_path), f"{config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read().strip()
    assert content == "SAFE_ORIGINAL_CONFIG", "system_config.txt was overwritten! Zip Slip vulnerability was not properly mitigated."

def test_nginx_flask_doc1():
    """Verify doc1.txt is served correctly with transformed GCODE."""
    url = "http://127.0.0.1:8080/docs/doc1.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for {url}, got {response.status_code}"

    expected_content = "Intro text.\n[GCODE]\nLINEAR_MOVE X:10 Y:20\nG0 Z5\n[/GCODE]\nEnd text."
    actual_content = response.text.strip()
    assert expected_content in actual_content or actual_content == expected_content, \
        f"Transformed content for doc1.txt is incorrect.\nExpected:\n{expected_content}\nGot:\n{actual_content}"

def test_nginx_flask_doc2():
    """Verify doc2.txt is served correctly with transformed GCODE."""
    url = "http://127.0.0.1:8080/docs/doc2.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for {url}, got {response.status_code}"

    expected_content = "[GCODE]\nLINEAR_MOVE X:50.5 Y:10.2\n[/GCODE]"
    actual_content = response.text.strip()
    assert expected_content in actual_content or actual_content == expected_content, \
        f"Transformed content for doc2.txt is incorrect.\nExpected:\n{expected_content}\nGot:\n{actual_content}"