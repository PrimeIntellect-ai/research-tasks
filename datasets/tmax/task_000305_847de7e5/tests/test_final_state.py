# test_final_state.py

import os
import time
import subprocess
import pytest
from packaging.version import Version

def test_project_structure():
    assert os.path.isdir("/home/user/project/src"), "Directory /home/user/project/src does not exist"
    assert os.path.isdir("/home/user/project/lib"), "Directory /home/user/project/lib does not exist"
    assert os.path.isdir("/home/user/project/data"), "Directory /home/user/project/data does not exist"

    assert os.path.isfile("/home/user/project/src/sort_versions.py"), "File /home/user/project/src/sort_versions.py missing"
    assert os.path.isfile("/home/user/project/lib/libsemver.so"), "File /home/user/project/lib/libsemver.so missing"
    assert os.path.isfile("/home/user/project/data/versions.txt"), "File /home/user/project/data/versions.txt missing"

def test_runtime_and_accuracy():
    script_path = "/home/user/project/src/sort_versions.py"
    data_path = "/home/user/project/data/versions.txt"
    out_path = "/home/user/project/data/sorted.txt"

    # Remove sorted.txt if it exists to ensure the script generates it during our test run
    if os.path.exists(out_path):
        os.remove(out_path)

    # Run the script and measure runtime
    start_time = time.time()
    result = subprocess.run(
        ["python3", "src/sort_versions.py"],
        cwd="/home/user/project",
        capture_output=True
    )
    runtime = time.time() - start_time

    assert result.returncode == 0, f"Script crashed. stderr: {result.stderr.decode()}"
    assert runtime <= 2.5, f"Runtime {runtime:.2f}s exceeds threshold of 2.5s."

    assert os.path.isfile(out_path), f"Output file {out_path} was not created by the script"

    # Compute ground truth
    with open(data_path, "r") as f:
        raw_versions = f.read().splitlines()

    ground_truth = sorted(raw_versions, key=Version, reverse=True)

    # Read agent's sorted output
    with open(out_path, "r") as f:
        agent_sorted = f.read().splitlines()

    assert len(agent_sorted) == len(ground_truth), f"Expected {len(ground_truth)} lines in sorted.txt, got {len(agent_sorted)}"

    # Calculate accuracy
    correct = sum(1 for a, b in zip(agent_sorted, ground_truth) if a == b)
    accuracy = correct / len(ground_truth)

    assert accuracy >= 0.99, f"Accuracy {accuracy:.4f} is below threshold of 0.99"