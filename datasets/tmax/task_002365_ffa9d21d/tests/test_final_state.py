# test_final_state.py
import os
import subprocess
import time
import pytest

def test_extracted_key():
    key_path = "/app/extracted_key.txt"
    assert os.path.isfile(key_path), f"File {key_path} does not exist. Did you extract the key?"

    with open(key_path, "r") as f:
        key = f.read().strip()

    expected_key = "AUTHKEY-9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d"
    assert key == expected_key, f"Incorrect key extracted. Expected '{expected_key}', got '{key}'."

def test_log_query_binary():
    bin_path = "/app/log-query-1.0/log-query"
    assert os.path.isfile(bin_path), f"Binary {bin_path} does not exist. Did you fix the Makefile and compile it?"
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

def test_final_timeline():
    timeline_path = "/app/final_timeline.txt"
    assert os.path.isfile(timeline_path), f"File {timeline_path} does not exist. Did you run the log-query tool?"
    assert os.path.getsize(timeline_path) > 0, f"File {timeline_path} is empty."

def test_recover_logs_metric():
    bin_path = "/app/recover_logs"
    if not os.path.isfile(bin_path):
        # Fallback to check if the user forgot to compile it but the source is there
        pytest.fail(f"Executable {bin_path} not found. Ensure you compile your C code to this exact path.")

    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

    input_img = "/hidden/large_partition.img"
    output_log = "/tmp/test_recovered.log"
    expected_log = "/hidden/expected.log"

    assert os.path.isfile(input_img), f"Hidden verifier file {input_img} is missing."
    assert os.path.isfile(expected_log), f"Hidden verifier file {expected_log} is missing."

    # Remove the output log if it exists from a previous run
    if os.path.exists(output_log):
        os.remove(output_log)

    start_time = time.time()
    proc = subprocess.run([bin_path, input_img, output_log], capture_output=True)
    elapsed = time.time() - start_time

    assert proc.returncode == 0, f"recover_logs failed with return code {proc.returncode}. stderr: {proc.stderr.decode('utf-8', errors='ignore')}"

    assert os.path.isfile(output_log), f"recover_logs did not create the output file at {output_log}."

    with open(output_log, "rb") as f:
        recovered = f.read()
    with open(expected_log, "rb") as f:
        expected = f.read()

    assert recovered == expected, "Recovered logs do not match the expected output exactly. (Accuracy < 1.0)"
    assert elapsed <= 1.0, f"Execution time {elapsed:.3f}s exceeds the 1.0s threshold."