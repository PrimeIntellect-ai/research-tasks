# test_final_state.py
import json
import time
import subprocess
import os
import pytest

def test_telemetry_pipeline():
    telemetry_dir = "/home/user/telemetry"

    # 1. Build the Go application
    build_res = subprocess.run(
        ["go", "build"], 
        cwd=telemetry_dir, 
        capture_output=True, 
        text=True
    )
    assert build_res.returncode == 0, f"Go build failed:\n{build_res.stderr}"

    # Ensure binary exists
    binary_path = os.path.join(telemetry_dir, "telemetry")
    assert os.path.exists(binary_path), "Compiled binary 'telemetry' not found."

    # Remove existing output.json if any, to ensure we test the fresh run
    output_path = os.path.join(telemetry_dir, "output.json")
    if os.path.exists(output_path):
        os.remove(output_path)

    # 2. Execute the compiled binary and measure time
    start_time = time.time()
    exec_res = subprocess.run(
        ["./telemetry"], 
        cwd=telemetry_dir, 
        capture_output=True, 
        text=True
    )
    duration = time.time() - start_time

    assert exec_res.returncode == 0, f"Execution of ./telemetry failed:\n{exec_res.stderr}"

    # 3. Check execution time threshold
    assert duration <= 3.0, f"Metric failed: Execution took {duration:.2f}s (Threshold <= 3.0s)"

    # 4. Check output.json
    assert os.path.exists(output_path), f"Output file not found at {output_path}"

    try:
        with open(output_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load JSON from {output_path}: {e}")

    # 5. Verify the number of records (validates race condition fix and proper filtering)
    expected_records = 9300
    actual_records = len(data)
    assert actual_records == expected_records, f"Expected {expected_records} valid records, got {actual_records}"