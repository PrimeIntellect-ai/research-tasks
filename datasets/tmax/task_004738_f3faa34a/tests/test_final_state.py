# test_final_state.py
import requests
import pytest
import time

def test_etl_server_response():
    """Test that the ETL server processes the logs correctly and returns the expected JSON."""
    url = "http://127.0.0.1:8080/ingest"
    headers = {
        "X-Batch-ID": "batch-9982-prod",
        "Content-Type": "text/plain"
    }
    payload = """[2023-10-12T10:00:00] [INFO] Database connection established successfully!
[2023-10-12T10:00:05] [ERROR] User login failed for username: admin.
[2023-10-12T10:00:08] [INFO] database connection established successfully
Invalid log line without timestamp
[2023-10-12T10:00:15] [ERROR] User login failed for username: root.
[2023-10-12T10:01:00] [WARN] Disk space running low"""

    expected_response = [
        {
            "timestamp": "2023-10-12T10:00:00",
            "level": "INFO",
            "cleaned_message": "database connection established successfully"
        },
        {
            "timestamp": "2023-10-12T10:00:05",
            "level": "ERROR",
            "cleaned_message": "user login failed for username admin"
        },
        {
            "timestamp": "2023-10-12T10:01:00",
            "level": "WARN",
            "cleaned_message": "disk space running low"
        }
    ]

    # Retry a few times in case the server is slow to start
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=5)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                pytest.fail("Could not connect to the server at 127.0.0.1:8080. Is it running?")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        actual_response = response.json()
    except ValueError:
        pytest.fail(f"Server did not return valid JSON. Response body: {response.text}")

    assert actual_response == expected_response, f"Expected JSON response {expected_response}, but got {actual_response}"