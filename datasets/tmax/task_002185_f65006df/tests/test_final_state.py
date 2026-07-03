# test_final_state.py

import os
import json
import subprocess
import time
import pytest

def test_recovered_json_state():
    """
    Validates that the recovered.json contains only the transactions up to 
    the last fully acknowledged TXN_ID (1045).
    """
    recovered_path = "/home/user/data/recovered.json"
    assert os.path.exists(recovered_path), f"File not found: {recovered_path}"

    try:
        with open(recovered_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {recovered_path} as JSON: {e}")

    expected_data = {
        "build_hash_A": "99283",
        "build_hash_B": "11223"
    }

    assert data == expected_data, (
        f"Recovered JSON state is incorrect.\n"
        f"Expected: {expected_data}\n"
        f"Got: {data}\n"
        f"Ensure you only parsed up to the last acknowledged TXN_ID."
    )

def test_server_throughput_and_leak_fix():
    """
    Starts the server, runs the load test to verify the resource leak is fixed,
    and checks if the throughput metric meets the requirement.
    """
    # Ensure any background instances left by the user are killed
    subprocess.run(["pkill", "-f", "async_build_cache.server"])
    time.sleep(1)

    # Start the server
    server_process = subprocess.Popen(
        ["python", "-m", "async_build_cache.server"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Give the server a moment to start
    time.sleep(2)

    try:
        # Run the throughput load test
        result = subprocess.run(
            ["python", "/home/user/verify_throughput.py"],
            capture_output=True,
            text=True,
            timeout=45
        )

        assert result.returncode == 0, (
            f"verify_throughput.py failed to run. This usually indicates the server "
            f"crashed or timed out due to the resource leak.\n"
            f"STDERR: {result.stderr}"
        )

        # The script is expected to print a single float representing req/sec
        output = result.stdout.strip().split('\n')[-1]
        try:
            throughput = float(output)
        except ValueError:
            pytest.fail(f"Could not parse throughput output as a float. Output was: {output}")

        assert throughput >= 800.0, (
            f"Throughput requirement not met. "
            f"Expected >= 800.0 req/sec, but got {throughput} req/sec. "
            f"The resource leak might not be fully fixed, or the server is spinning."
        )

    finally:
        # Cleanup the server process
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()