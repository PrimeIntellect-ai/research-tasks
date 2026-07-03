# test_final_state.py

import os
import time
import subprocess
import numpy as np
import pytest

def test_run_service_performance_and_correctness():
    script_path = "/home/user/run_service.py"
    assert os.path.exists(script_path), f"Student script not found at {script_path}"

    output_path = "/home/user/output.bin"
    if os.path.exists(output_path):
        os.remove(output_path)

    # Measure the execution time of the student's script
    start_time = time.time()
    proc = subprocess.run(["python3", script_path], capture_output=True, text=True)
    end_time = time.time()
    runtime = end_time - start_time

    assert proc.returncode == 0, f"Python script failed with return code {proc.returncode}. stderr: {proc.stderr}"
    assert os.path.exists(output_path), f"Output file not created at {output_path}"

    # Read the generated output
    with open(output_path, "rb") as f:
        result_data = f.read()

    dataset_path = "/app/dataset.bin"
    assert os.path.exists(dataset_path), f"Dataset file missing at {dataset_path}"

    # Efficiently compute the expected XOR transformation using numpy
    with open(dataset_path, "rb") as f:
        dataset_arr = np.frombuffer(f.read(), dtype=np.uint8)

    expected_data = np.bitwise_xor(dataset_arr, 0xAA).tobytes()

    # Verify correctness and performance metric
    assert result_data == expected_data, "Output data does not match expected XOR transformation"
    assert runtime <= 3.0, f"Performance threshold failed: runtime {runtime:.2f}s > 3.0s"