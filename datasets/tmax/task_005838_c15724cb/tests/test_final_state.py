# test_final_state.py
import os
import re

def test_results_log_exists():
    """Test that the results.log file was created."""
    log_path = '/home/user/pipeline/results.log'
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did the script run and save the output?"

def test_results_log_contents():
    """Test that the results.log file contains the correct computed Mean and StdDev."""
    log_path = '/home/user/pipeline/results.log'
    assert os.path.isfile(log_path), f"Missing {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    # Extract Mean
    mean_match = re.search(r'Mean:\s*([0-9\.\-]+)', content, re.IGNORECASE)
    assert mean_match is not None, "Could not find 'Mean: <value>' in results.log. Ensure the format exactly matches."
    mean_val = float(mean_match.group(1))
    assert abs(mean_val - 0.1693) < 0.0002, f"Expected Mean to be approximately 0.1693, got {mean_val}"

    # Extract StdDev
    std_match = re.search(r'StdDev:\s*([0-9\.\-]+)', content, re.IGNORECASE)
    assert std_match is not None, "Could not find 'StdDev: <value>' in results.log. Ensure the format exactly matches."
    std_val = float(std_match.group(1))
    assert abs(std_val - 83.1843) < 0.0002, f"Expected StdDev to be approximately 83.1843, got {std_val}"

def test_process_spectra_fixed():
    """Test that the process_spectra.py script no longer uses the failing Cholesky decomposition."""
    script_path = '/home/user/pipeline/process_spectra.py'
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'cholesky' not in content.lower(), "The script still contains 'cholesky'. The failing Cholesky decomposition must be removed and replaced with an SVD/pseudo-inverse approach."