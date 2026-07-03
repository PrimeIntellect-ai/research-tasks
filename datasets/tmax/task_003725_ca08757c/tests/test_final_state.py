# test_final_state.py
import os
import requests
import json
import time

def test_filter_executable_exists():
    """Verify that the filter executable was successfully built."""
    filter_path = "/home/user/service/filter"
    assert os.path.isfile(filter_path), f"The executable {filter_path} is missing. Did you run make?"
    assert os.access(filter_path, os.X_OK), f"The file {filter_path} is not executable."

def test_server_log_exists():
    """Verify that the server log file was created."""
    log_path = "/home/user/server.log"
    assert os.path.isfile(log_path), f"The server log file {log_path} is missing."

def test_server_transcribe_endpoint():
    """Verify that the server is running and returns the correct response format and transcript."""
    url = "http://127.0.0.1:8888/api/v1/transcribe"

    # Attempt to connect to the server, with a short retry in case it's slow to respond
    max_retries = 3
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            break
        except requests.exceptions.RequestException as e:
            if i == max_retries - 1:
                assert False, f"Failed to connect to the server at {url}: {e}"
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON. Response text: {response.text}"

    assert "version" in data, "Response JSON is missing the 'version' key"
    assert data["version"] == "v2", f"Expected version 'v2', got '{data['version']}'"

    assert "data" in data, "Response JSON is missing the 'data' key"
    assert "status" in data["data"], "Response JSON is missing the 'data.status' key"
    assert data["data"]["status"] == "success", f"Expected status 'success', got '{data['data']['status']}'"

    assert "transcript" in data["data"], "Response JSON is missing the 'data.transcript' key"
    transcript = data["data"]["transcript"].lower()
    expected_phrase = "open the pod bay doors"
    assert expected_phrase in transcript, f"Expected transcript to contain '{expected_phrase}', but got '{transcript}'"