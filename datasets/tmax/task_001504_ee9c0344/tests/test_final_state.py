# test_final_state.py

import pytest
import requests
import subprocess
import time

def get_redis_list(list_name):
    """Retrieve all elements from a Redis list."""
    try:
        result = subprocess.run(
            ["redis-cli", "LRANGE", list_name, "0", "-1"],
            capture_output=True, text=True, check=True
        )
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis for {list_name}: {e.stderr}")

def test_end_to_end_telemetry():
    """Verify that the proxy and backend correctly route and process telemetry data."""
    # Clear the Redis lists to ensure a clean state for testing
    subprocess.run(["redis-cli", "DEL", "releases:valid", "releases:invalid"], check=True)

    # Define test cases: (payload, expected_redis_list, expected_data_string)
    test_cases = [
        ("v2.5.0|success_deploy", "releases:valid", "success_deploy"),
        ("1.1.9|fail_deploy", "releases:invalid", "fail_deploy"),
        ("2.0.0|edge_valid", "releases:valid", "edge_valid"),
        ("v1.9.9|edge_invalid", "releases:invalid", "edge_invalid"),
        ("10.0.0|future_deploy", "releases:valid", "future_deploy"),
    ]

    # Send requests to the Go proxy
    for payload, expected_list, expected_data in test_cases:
        try:
            resp = requests.post("http://127.0.0.1:8080/", data=payload, timeout=2)
            assert resp.status_code == 200, f"Expected HTTP 200 from proxy, got {resp.status_code} for payload: {payload}"
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to the Go proxy on 127.0.0.1:8080. Is it running? Error: {e}")

    # Allow a brief moment for the C backend to process and push to Redis asynchronously
    time.sleep(0.5)

    valid_list = get_redis_list("releases:valid")
    invalid_list = get_redis_list("releases:invalid")

    # Verify the contents of the Redis lists
    for payload, expected_list, expected_data in test_cases:
        if expected_list == "releases:valid":
            assert expected_data in valid_list, (
                f"Expected '{expected_data}' in Redis list 'releases:valid' (from payload '{payload}'). "
                f"Actual contents: {valid_list}"
            )
        else:
            assert expected_data in invalid_list, (
                f"Expected '{expected_data}' in Redis list 'releases:invalid' (from payload '{payload}'). "
                f"Actual contents: {invalid_list}"
            )