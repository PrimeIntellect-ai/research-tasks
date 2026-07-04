# test_final_state.py

import os
import time
import subprocess
import numpy as np

def test_fast_pipeline():
    script_path = '/home/user/event_pipeline/fast_pipeline.py'
    input_file = '/home/user/data/events.bin'
    output_file = '/home/user/event_pipeline/output.bin'
    legacy_engine = '/app/legacy_engine'

    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Remove output file if it exists to ensure we measure the new run
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run the user script and measure time
    start_time = time.time()
    result = subprocess.run(['python3', script_path, input_file, output_file], capture_output=True, text=True)
    end_time = time.time()

    runtime = end_time - start_time

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert os.path.isfile(output_file), f"Output file not created at {output_file}"

    # Run the legacy engine to get the ground truth
    with open(input_file, 'rb') as f:
        legacy_result = subprocess.run([legacy_engine], stdin=f, capture_output=True)

    assert legacy_result.returncode == 0, f"Legacy engine failed to process input. Stderr: {legacy_result.stderr}"
    expected_output = legacy_result.stdout

    # Read the actual output
    with open(output_file, 'rb') as f:
        actual_output = f.read()

    # Calculate MSE
    # Both are binary arrays of 16-bit integers
    expected_array = np.frombuffer(expected_output, dtype=np.int16)
    actual_array = np.frombuffer(actual_output, dtype=np.int16)

    assert len(expected_array) == len(actual_array), f"Output length mismatch: expected {len(expected_array)} elements, got {len(actual_array)} elements"

    if len(expected_array) > 0:
        mse = np.mean((expected_array.astype(np.float64) - actual_array.astype(np.float64)) ** 2)
    else:
        mse = 0.0

    assert mse == 0.0, f"Output MSE vs reference is {mse}, expected 0.0"
    assert runtime < 1.5, f"Runtime speed is {runtime:.3f} seconds, expected < 1.5 seconds"