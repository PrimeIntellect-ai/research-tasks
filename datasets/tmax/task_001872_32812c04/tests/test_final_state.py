# test_final_state.py

import os
import subprocess
import pytest

def test_evaluation_summary_exists():
    """Check if the evaluation summary file was created."""
    summary_path = '/home/user/evaluation_summary.txt'
    assert os.path.isfile(summary_path), f"File {summary_path} does not exist."

def test_evaluation_summary_content():
    """Verify the content of the evaluation summary exactly matches the expected computation."""
    summary_path = '/home/user/evaluation_summary.txt'

    # Recompute the expected output using the exact logic specified in the task
    # This ensures we match GNU shuf's exact sampling behavior given the random seed
    cmd = (
        "grep -E '^[^,]+,[0-9.]+,[0-9.]+,[0-9.]+$' /home/user/artifacts.csv | "
        "shuf -n 30 --random-source=/home/user/random_seed | "
        "awk -F',' '{sum_acc+=$2; sum_loss+=$3} END "
        "{printf \"Mean Accuracy: %.4f, Mean Loss: %.4f\\n\", sum_acc/NR, sum_loss/NR}'"
    )

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        expected_content = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected truth data: {e.stderr}")

    # Read the student's output
    with open(summary_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {summary_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{actual_content}'"
    )