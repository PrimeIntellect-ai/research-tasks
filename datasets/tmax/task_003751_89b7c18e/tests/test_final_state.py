# test_final_state.py

import json
import math
import socket
import pytest
import requests

def test_rust_service_and_redis():
    # Payload to send
    payload = [[10.0, 20.0], [20.0, 20.0], [30.0, 80.0]]

    try:
        response = requests.post("http://127.0.0.1:3000/prepare", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Rust web service at 127.0.0.1:3000. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response from the Rust service. Response: {response.text}")

    assert "original" in data, "Response JSON missing 'original' key"
    assert "bootstraps" in data, "Response JSON missing 'bootstraps' key"

    original = data["original"]
    bootstraps = data["bootstraps"]

    assert len(original) == 3, f"Expected 3 rows in 'original', got {len(original)}"
    assert len(original[0]) == 2, f"Expected 2 columns in 'original', got {len(original[0])}"
    assert len(bootstraps) == 5, f"Expected 5 bootstraps, got {len(bootstraps)}"

    # Check scaling. Could be population or sample std dev.
    # Original data:
    # col 0: 10, 20, 30. Mean: 20.
    # col 1: 20, 20, 80. Mean: 40.
    # Pop std: col 0 = 8.1649658, col 1 = 28.284271
    # Sample std: col 0 = 10.0, col 1 = 34.641016

    # Let's see what the first element is to determine which scaling was used.
    val_0_0 = original[0][0]

    if math.isclose(val_0_0, -1.224744871391589, rel_tol=1e-3):
        # Population std dev
        std_0 = math.sqrt(200 / 3)
        std_1 = math.sqrt(800)
    elif math.isclose(val_0_0, -1.0, rel_tol=1e-3):
        # Sample std dev
        std_0 = 10.0
        std_1 = math.sqrt(1200)
    else:
        pytest.fail(f"Scaling is incorrect. Expected first element to be approx -1.2247 (pop std) or -1.0 (sample std), got {val_0_0}")

    expected_original = [
        [(10.0 - 20.0) / std_0, (20.0 - 40.0) / std_1],
        [(20.0 - 20.0) / std_0, (20.0 - 40.0) / std_1],
        [(30.0 - 20.0) / std_0, (80.0 - 40.0) / std_1],
    ]

    for i in range(3):
        for j in range(2):
            assert math.isclose(original[i][j], expected_original[i][j], rel_tol=1e-3, abs_tol=1e-4), \
                f"Mismatch in 'original' at [{i}][{j}]. Expected {expected_original[i][j]}, got {original[i][j]}"

    # Check bootstraps
    for b_idx, boot in enumerate(bootstraps):
        assert len(boot) == 3, f"Expected 3 rows in bootstrap {b_idx}, got {len(boot)}"
        for r_idx, row in enumerate(boot):
            assert len(row) == 2, f"Expected 2 columns in bootstrap {b_idx} row {r_idx}, got {len(row)}"
            # Each row in bootstrap must be one of the expected_original rows
            matched = False
            for exp_row in expected_original:
                if math.isclose(row[0], exp_row[0], rel_tol=1e-3, abs_tol=1e-4) and \
                   math.isclose(row[1], exp_row[1], rel_tol=1e-3, abs_tol=1e-4):
                    matched = True
                    break
            assert matched, f"Bootstrap {b_idx} row {r_idx} ({row}) does not match any correctly scaled original row. Data leak might still exist."

    # Calculate expected max absolute value
    max_abs_val = max(abs(val) for row in expected_original for val in row)

    # Check Redis
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(("127.0.0.1", 6379))
        s.sendall(b"*2\r\n$3\r\nGET\r\n$27\r\nexperiment:latest:max_abs_val\r\n")
        resp = s.recv(1024).decode("utf-8")
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to Redis at 127.0.0.1:6379 or execute GET. Is it running? Error: {e}")

    # RESP bulk string response format: $<length>\r\n<data>\r\n
    lines = resp.split("\r\n")
    if len(lines) < 2 or lines[0].startswith("$-1"):
        pytest.fail(f"Redis key 'experiment:latest:max_abs_val' not found or empty. Raw response: {repr(resp)}")

    redis_val_str = lines[1]
    try:
        redis_val = float(redis_val_str)
    except ValueError:
        pytest.fail(f"Redis value '{redis_val_str}' is not a valid float.")

    assert math.isclose(redis_val, max_abs_val, rel_tol=1e-3, abs_tol=1e-4), \
        f"Redis max_abs_val mismatch. Expected approx {max_abs_val}, got {redis_val}"