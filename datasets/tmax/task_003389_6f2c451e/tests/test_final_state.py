# test_final_state.py

import os
import json
import socket
import urllib.request
import pytest
import math

def test_mre_json():
    path = "/home/user/mre.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            mre_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(mre_data, list), f"Expected {path} to contain a JSON array."
    expected_mre = [10000000000.0, 10000000000.1, 10000000000.2]
    assert mre_data == expected_mre, f"MRE sequence in {path} does not match the expected minimal sequence."

def test_resolution_json():
    path = "/home/user/resolution.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            res_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "variance" in res_data, f"'variance' key missing in {path}."
    variance = res_data["variance"]
    assert isinstance(variance, (int, float)), f"'variance' is not a number in {path}."

    expected_variance = 0.006666666666666667
    assert math.isclose(variance, expected_variance, rel_tol=1e-3, abs_tol=1e-5), \
        f"Variance {variance} in {path} is incorrect. Expected approximately {expected_variance}."

def test_trace_log():
    path = "/home/user/trace.log"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 3, f"Expected at least 3 lines in {path}."

    # We look for the last 3 lines assuming the user restarted the server and sent the MRE
    last_3_lines = lines[-3:]

    # Expected substrings based on the MRE sequence
    expected_patterns = [
        "Count: 1",
        "Count: 2",
        "Count: 3"
    ]

    for i, pattern in enumerate(expected_patterns):
        assert pattern in last_3_lines[i], f"Expected '{pattern}' in log line: {last_3_lines[i]}"

    # Check if Welford's M2 and Variance are logged in the last line
    last_line = last_3_lines[-1]
    assert "Mean:" in last_line, f"Missing 'Mean:' in log line: {last_line}"
    assert "M2:" in last_line, f"Missing 'M2:' in log line: {last_line}"
    assert "Variance:" in last_line, f"Missing 'Variance:' in log line: {last_line}"

def test_server_running_and_fixed():
    # Check if port 8080 is open
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "Server is not listening on port 8080."

    # Reset the server state
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/reset", method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, "Failed to reset server state."
    except Exception as e:
        pytest.fail(f"Could not reach /reset endpoint: {e}")

    # Send the MRE sequence to verify the server calculation is fixed
    mre_sequence = [10000000000.0, 10000000000.1, 10000000000.2]
    last_variance = None

    for val in mre_sequence:
        payload = json.dumps({"value": val}).encode("utf-8")
        req = urllib.request.Request("http://127.0.0.1:8080/metric", data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, "Failed to send metric."
                resp_data = json.loads(response.read().decode())
                last_variance = resp_data.get("variance")
        except Exception as e:
            pytest.fail(f"Could not send metric to server: {e}")

    assert last_variance is not None, "Server did not return a variance."
    expected_variance = 0.006666666666666667
    assert math.isclose(last_variance, expected_variance, rel_tol=1e-3, abs_tol=1e-5), \
        f"Server returned incorrect variance {last_variance}. Expected approximately {expected_variance}."