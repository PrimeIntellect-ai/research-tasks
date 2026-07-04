# test_final_state.py

import os
import pytest

def test_script_exists():
    """Check if the analyze_metrics.py script exists."""
    script_path = "/home/user/analyze_metrics.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_results_txt():
    """Check if results.txt exists and contains the correct output."""
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"Results file {results_path} is missing."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_content = "closest_server: srv_beta\np_value: 0.0248"

    # Normalize line endings and whitespace for robust comparison
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {results_path} do not match the expected output. Got:\n{content}"

def test_histogram_png():
    """Check if histogram.png exists and is a non-empty file."""
    image_path = "/home/user/histogram.png"
    assert os.path.exists(image_path), f"Image file {image_path} is missing."
    assert os.path.isfile(image_path), f"{image_path} is not a file."
    assert os.path.getsize(image_path) > 0, f"Image file {image_path} is empty."