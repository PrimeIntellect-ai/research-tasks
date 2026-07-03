# test_final_state.py
import os
import re
import pytest

def test_analyze_script_exists():
    """Verify that the analyze.py script was created."""
    script_path = '/home/user/analyze.py'
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

def test_results_file_exists():
    """Verify that the results.txt file was created."""
    results_path = '/home/user/results.txt'
    assert os.path.isfile(results_path), f"Results file missing: {results_path}"

def test_results_content():
    """Verify the contents of results.txt match the expected output."""
    results_path = '/home/user/results.txt'

    with open(results_path, 'r') as f:
        content = f.read()

    dist_match = re.search(r'Distance:\s*([\d.]+)', content)
    lower_match = re.search(r'CI_Lower:\s*([\d.]+)', content)
    upper_match = re.search(r'CI_Upper:\s*([\d.]+)', content)

    assert dist_match is not None, "Could not find 'Distance: <value>' format in results.txt"
    assert lower_match is not None, "Could not find 'CI_Lower: <value>' format in results.txt"
    assert upper_match is not None, "Could not find 'CI_Upper: <value>' format in results.txt"

    dist = float(dist_match.group(1))
    lower = float(lower_match.group(1))
    upper = float(upper_match.group(1))

    # Allow a tiny bit of floating point tolerance due to string rounding
    assert abs(dist - 0.5218) <= 1e-4, f"Expected Distance to be 0.5218, got {dist:.4f}"
    assert abs(lower - 0.3957) <= 1e-4, f"Expected CI_Lower to be 0.3957, got {lower:.4f}"
    assert abs(upper - 0.6559) <= 1e-4, f"Expected CI_Upper to be 0.6559, got {upper:.4f}"