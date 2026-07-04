# test_final_state.py
import os
import time
import requests

def test_server_script_exists():
    server_script = "/home/user/app/server.py"
    assert os.path.isfile(server_script), f"Server script {server_script} does not exist."

def test_http_endpoint_responses():
    url = "http://127.0.0.1:8080/latest-events"

    # Make multiple requests to ensure stability against race conditions (log rotation)
    for i in range(3):
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            assert False, f"Failed to connect to the server at {url}. Error: {e}"

        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

        try:
            data = response.json()
        except ValueError:
            assert False, "Response body is not valid JSON."

        assert isinstance(data, list), "Expected response JSON to be a list."

        if data:
            # Verify the structure of the parsed items
            last_item = data[-1]
            assert "event_id" in last_item, f"Expected 'event_id' in record, got {last_item}"
            assert "status" in last_item, f"Expected 'status' in record, got {last_item}"

        time.sleep(1.5) # Wait to allow the background writer to write/rotate