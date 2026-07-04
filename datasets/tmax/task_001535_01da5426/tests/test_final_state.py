# test_final_state.py

import os
import time
import subprocess
import pytest

def test_token_generator_source_exists():
    assert os.path.isfile('/home/user/token_generator.cpp'), "The C++ source file /home/user/token_generator.cpp is missing."

def test_token_generator_binary_exists():
    assert os.path.isfile('/home/user/token_generator'), "The compiled binary /home/user/token_generator is missing."
    assert os.access('/home/user/token_generator', os.X_OK), "The file /home/user/token_generator is not executable."

def test_success_log_contains_flag():
    log_path = '/home/user/success.log'
    assert os.path.isfile(log_path), f"The success log file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read()

    assert "FLAG{bypass_successful_9921}" in content, "The success.log does not contain the expected flag. The bypass may have failed."

def test_generator_performance_metric():
    binary_path = '/home/user/token_generator'
    assert os.path.isfile(binary_path), f"Binary {binary_path} not found for performance test."

    # Define the metric threshold
    threshold = 0.8
    num_tokens = "1000000"
    payload = "role=admin"

    start_time = time.time()
    try:
        result = subprocess.run(
            [binary_path, num_tokens, payload],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {binary_path} failed with return code {e.returncode}. Stderr: {e.stderr}")

    duration = time.time() - start_time

    # Assert the metric against the threshold
    assert duration <= threshold, f"Performance metric failed: Execution time was {duration:.4f} seconds, which exceeds the threshold of {threshold} seconds."

    # Verify the output file was created
    output_path = '/home/user/tokens.txt'
    assert os.path.isfile(output_path), f"The expected output file {output_path} was not created by the generator."

    # Optionally, verify the number of lines in the output file
    # We use a simple count to ensure it generated the expected number of tokens
    with open(output_path, 'rb') as f:
        num_lines = sum(1 for _ in f)

    assert num_lines == int(num_tokens), f"The output file {output_path} contains {num_lines} tokens, expected {num_tokens}."