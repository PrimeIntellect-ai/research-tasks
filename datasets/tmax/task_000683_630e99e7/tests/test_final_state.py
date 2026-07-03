# test_final_state.py
import os
import subprocess
import time
import requests
import math
import pytest

def test_run_server_script_exists():
    assert os.path.isfile("/home/user/run_server.sh"), "run_server.sh does not exist"
    assert os.access("/home/user/run_server.sh", os.X_OK), "run_server.sh is not executable"

def test_server_response():
    # Start the server
    process = subprocess.Popen(
        ["/bin/bash", "/home/user/run_server.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/home/user"
    )

    try:
        # Wait for the server to start
        server_up = False
        for _ in range(30):
            try:
                response = requests.get("http://127.0.0.1:8080/embedding", timeout=1)
                if response.status_code == 200:
                    server_up = True
                    break
            except requests.exceptions.RequestException:
                time.sleep(1)

        assert server_up, "Server did not start or did not respond with 200 OK on /embedding within 30 seconds."

        data = response.json()
        assert "mean" in data, "Response JSON missing 'mean'"
        assert "std" in data, "Response JSON missing 'std'"
        assert "embedding" in data, "Response JSON missing 'embedding'"

        mean = float(data["mean"])
        std = float(data["std"])
        embedding = data["embedding"]

        assert isinstance(embedding, list), "'embedding' should be a list"
        assert len(embedding) == 5, f"Expected 5 embedding values, got {len(embedding)}"

        # Original values
        expected_values = [12, 15, 22, 29, 35]

        # Check mean
        assert math.isclose(mean, 22.6, rel_tol=0.05), f"Expected mean ~22.6, got {mean}"

        # Check std (could be population ~8.54 or sample ~9.55, prompt says ~8.35, so we allow a generous range)
        assert 7.0 < std < 10.0, f"Standard deviation {std} is outside expected range"

        # Check embedding math
        for i, val in enumerate(expected_values):
            expected_z = (val - mean) / std
            assert math.isclose(embedding[i], expected_z, rel_tol=0.1, abs_tol=0.1), \
                f"Embedding at index {i} expected ~{expected_z}, got {embedding[i]}"

    finally:
        # Cleanup
        process.terminate()
        process.wait(timeout=5)
        # Kill any lingering processes on port 8080
        subprocess.run(["fuser", "-k", "8080/tcp"], capture_output=True)