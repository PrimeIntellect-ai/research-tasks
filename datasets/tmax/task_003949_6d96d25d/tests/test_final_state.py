# test_final_state.py

import os
import subprocess
import time

def test_parser_exists_and_executable():
    path = "/home/user/parser/parser"
    assert os.path.isfile(path), f"Compiled binary not found at {path}"
    assert os.access(path, os.X_OK), f"Binary at {path} is not executable"

def test_execution_time_and_accuracy():
    binary_path = "/home/user/parser/parser"
    input_path = "/app/mem_dump.bin"
    output_path = "/home/user/extracted_strings.txt"

    # Ensure binary exists before running
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"

    # Generate expected strings logically based on the setup
    expected_strings = "\n".join(f"ValidString_{i}" for i in range(50))

    # Remove output file if it exists to ensure we are testing the new run
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the binary and measure execution time
    start_time = time.time()
    res = subprocess.run([binary_path, input_path, output_path], capture_output=True)
    elapsed = time.time() - start_time

    # Check for crash or error
    assert res.returncode == 0, f"Parser failed with return code {res.returncode}. Stderr: {res.stderr.decode('utf-8', errors='replace')}"

    # Check if output file was created
    assert os.path.isfile(output_path), f"Output file not created at {output_path}"

    # Verify the contents of the output file
    with open(output_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_strings, "The extracted strings do not match the expected output. Ensure the delimiter, offset, and bounds checking are correct."

    # Verify the performance metric
    threshold = 0.2
    assert elapsed <= threshold, f"Execution time {elapsed:.4f}s exceeded the threshold of {threshold}s. The I/O operations are likely still inefficient."