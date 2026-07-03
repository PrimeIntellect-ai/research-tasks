# test_final_state.py

import os
import subprocess
from collections import defaultdict

def test_pipeline_exists_and_executable():
    """Verify that pipeline.sh exists and is executable."""
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"The file {pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"The file {pipeline_path} is not executable."

def test_run_pipeline():
    """Run the pipeline.sh script and ensure it succeeds."""
    pipeline_path = "/home/user/pipeline.sh"
    result = subprocess.run([pipeline_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_anomaly_samples_output():
    """Verify that anomaly_samples.csv is created and has the correct contents."""
    output_path = "/home/user/anomaly_samples.csv"
    log_path = "/home/user/server_logs.txt"

    assert os.path.isfile(output_path), f"The output file {output_path} was not created."
    assert os.path.isfile(log_path), f"The input log file {log_path} is missing."

    # Compute expected output based on the truth logic
    records = []
    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            parts = line.split()
            # [YYYY-MM-DD HH:MM:SS] IP_ADDRESS HTTP_METHOD ENDPOINT STATUS_CODE RESPONSE_TIME_MS USER_AGENT
            # parts[0] = [YYYY-MM-DD
            # parts[1] = HH:MM:SS]
            # parts[2] = IP_ADDRESS
            # parts[3] = HTTP_METHOD
            # parts[4] = ENDPOINT
            # parts[5] = STATUS_CODE
            # parts[6] = RESPONSE_TIME_MS
            # parts[7] = USER_AGENT
            status = int(parts[5])
            time_ms = int(parts[6])
            score = time_ms * 2 if status >= 400 else time_ms
            records.append((status, score, line))

    stratified = defaultdict(list)
    for r in records:
        stratified[r[0]].append(r)

    final_output = []
    for status in sorted(stratified.keys()):
        # Sort by score descending. If there are ties, Python's stable sort keeps original order, 
        # but the task doesn't specify tie-breaking logic. We'll just sort by score descending.
        top5 = sorted(stratified[status], key=lambda x: x[1], reverse=True)[:5]
        final_output.extend(top5)

    expected_lines = ["StatusCode,AnomalyScore,OriginalLogLine"]
    for r in final_output:
        expected_lines.append(f"{r[0]},{r[1]},{r[2]}")

    # Read actual output
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), \
        f"Output file has {len(actual_lines)} lines, but expected {len(expected_lines)} lines."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, \
            f"Mismatch at line {i+1} in {output_path}.\nExpected: {expected}\nActual:   {actual}"