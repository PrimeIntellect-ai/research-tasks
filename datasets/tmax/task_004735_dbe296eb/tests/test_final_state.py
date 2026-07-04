# test_final_state.py

import os
import time
import subprocess
import pytest

def test_safe_analyzer_performance_and_accuracy():
    script_path = "/home/user/safe_analyzer.py"
    input_logs = "/app/held_out_logs.txt"
    golden_scores_file = "/app/golden_scores.txt"

    assert os.path.exists(script_path), f"File not found: {script_path}"
    assert os.path.exists(input_logs), f"File not found: {input_logs}"
    assert os.path.exists(golden_scores_file), f"File not found: {golden_scores_file}"

    with open(input_logs, 'r') as f:
        num_lines = sum(1 for _ in f)

    start_time = time.time()
    try:
        with open(input_logs, 'r') as stdin_f:
            result = subprocess.run(
                ["python3", script_path],
                stdin=stdin_f,
                capture_output=True,
                text=True,
                timeout=60
            )
    except subprocess.TimeoutExpired:
        pytest.fail("safe_analyzer.py timed out. It did not process the logs fast enough, indicating the hang is still present.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    assert result.returncode == 0, f"safe_analyzer.py failed with error:\n{result.stderr}"

    output_lines = result.stdout.strip().split('\n')
    output_lines = [line for line in output_lines if line.strip()]

    with open(golden_scores_file, 'r') as f:
        golden_lines = f.read().strip().split('\n')
        golden_lines = [line for line in golden_lines if line.strip()]

    assert len(output_lines) == len(golden_lines), f"Expected {len(golden_lines)} output scores, got {len(output_lines)}"

    mse = 0.0
    for out_val, gold_val in zip(output_lines, golden_lines):
        try:
            o = float(out_val)
            g = float(gold_val)
            mse += (o - g) ** 2
        except ValueError:
            pytest.fail(f"Could not parse output as float: {out_val}")

    mse /= len(golden_lines)

    throughput = num_lines / elapsed_time if elapsed_time > 0 else float('inf')

    assert throughput > 500, f"Throughput too low: {throughput:.2f} lines/sec (threshold > 500)"
    assert mse < 0.05, f"MSE too high: {mse:.4f} (threshold < 0.05)"