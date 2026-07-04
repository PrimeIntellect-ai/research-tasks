# test_final_state.py
import os
import re
import subprocess
import pytest

def test_analyze_primers_fixed():
    path = "/home/user/analyze_primers.py"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    # Check that SVD is used
    assert 'svd' in content.lower(), "SVD is not used in analyze_primers.py"

    # Check that it runs successfully on the first batch
    batch_file = "/home/user/data/batch_1.txt"
    assert os.path.exists(batch_file), f"Data file {batch_file} is missing."

    result = subprocess.run(
        ["python3", path, batch_file],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"analyze_primers.py failed to run: {result.stderr}"
    assert "Result:" in result.stdout, "analyze_primers.py did not print 'Result:'"

def test_times_txt():
    path = "/home/user/times.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"{path} should contain exactly 100 lines, found {len(lines)}"

    for i, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line {i+1} in {path} is not a valid float: '{line}'")

def test_fit_density_exists():
    path = "/home/user/fit_density.py"
    assert os.path.exists(path), f"File {path} does not exist."

def test_profile_results():
    path = "/home/user/profile_results.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    mean_match = re.search(r'^Mean:\s*(-?\d+\.\d{4})$', content, re.MULTILINE)
    std_match = re.search(r'^Std:\s*(\d+\.\d{4})$', content, re.MULTILINE)

    assert mean_match is not None, "profile_results.txt does not contain 'Mean: <value>' with 4 decimal places."
    assert std_match is not None, "profile_results.txt does not contain 'Std: <value>' with 4 decimal places."

    # Verify the values actually match the times.txt data
    times_path = "/home/user/times.txt"
    if os.path.exists(times_path):
        with open(times_path, 'r') as f:
            times = [float(line.strip()) for line in f if line.strip()]

        if len(times) > 0:
            import statistics
            expected_mean = statistics.mean(times)
            # Use population std dev to closely mimic scipy.stats.norm.fit which uses MLE (n, not n-1)
            expected_std = statistics.pstdev(times)

            actual_mean = float(mean_match.group(1))
            actual_std = float(std_match.group(1))

            assert abs(actual_mean - expected_mean) < 1e-3, f"Expected mean ~{expected_mean:.4f}, got {actual_mean}"
            assert abs(actual_std - expected_std) < 1e-3, f"Expected std ~{expected_std:.4f}, got {actual_std}"