# test_final_state.py

import os
import subprocess
import re
import pytest

def test_generate_plan_script_exists():
    script_path = "/home/user/generate_plan.py"
    assert os.path.exists(script_path), f"Missing required script at {script_path}"
    assert os.path.isfile(script_path), f"Path {script_path} is not a file"

def test_backup_plan_exists_and_meets_latency_threshold():
    plan_path = "/home/user/backup_plan.json"
    binary_path = "/app/backup_scheduler"

    assert os.path.exists(plan_path), f"Missing backup plan at {plan_path}"
    assert os.path.isfile(plan_path), f"Path {plan_path} is not a file"
    assert os.path.exists(binary_path), f"Missing binary at {binary_path}"

    # Run the backup scheduler with the generated plan
    try:
        result = subprocess.run(
            [binary_path, plan_path],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Backup scheduler failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    output = result.stdout

    # Parse the latency from the output
    match = re.search(r"Total Latency:\s*(\d+)\s*ms", output, re.IGNORECASE)
    assert match is not None, f"Could not find 'Total Latency: <number> ms' in output:\n{output}"

    latency = int(match.group(1))
    threshold = 1500

    assert latency <= threshold, f"Latency metric failed: measured {latency} ms, which is > threshold {threshold} ms"