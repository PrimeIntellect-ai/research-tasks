# test_final_state.py

import os
import re
import stat
import pytest

RESULTS_FILE = "/home/user/results.txt"
BASH_SCRIPT = "/home/user/run_analysis.sh"
PYTHON_SCRIPT = "/home/user/analyze.py"

def test_bash_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    assert os.path.isfile(BASH_SCRIPT), f"Missing bash script: {BASH_SCRIPT}"
    st = os.stat(BASH_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script is not executable: {BASH_SCRIPT}"

def test_results_file_exists():
    """Test that the results file was created."""
    assert os.path.isfile(RESULTS_FILE), f"Missing results file: {RESULTS_FILE}"

def test_results_content():
    """Test that the results file contains the correct values."""
    with open(RESULTS_FILE, "r") as f:
        content = f.read().strip()

    # Check for Peak Center
    peak_match = re.search(r"Peak Center:\s*([0-9.]+)", content, re.IGNORECASE)
    assert peak_match, "Could not find 'Peak Center: <value>' in results.txt"
    peak_val = float(peak_match.group(1))
    assert abs(peak_val - 4.234567) < 1e-5, f"Expected Peak Center near 4.234567, got {peak_val}"

    # Check for Total Area
    area_match = re.search(r"Total Area:\s*([0-9.]+)", content, re.IGNORECASE)
    assert area_match, "Could not find 'Total Area: <value>' in results.txt"
    area_val = float(area_match.group(1))
    assert abs(area_val - 1.500000) < 1e-5, f"Expected Total Area near 1.500000, got {area_val}"

def test_no_forbidden_functions():
    """Test that the python script does not use scipy.integrate.quad."""
    assert os.path.isfile(PYTHON_SCRIPT), f"Missing python script: {PYTHON_SCRIPT}"
    with open(PYTHON_SCRIPT, "r") as f:
        content = f.read()

    assert "scipy.integrate" not in content or "quad" not in content, "The use of scipy.integrate.quad is forbidden. You must use the provided adaptive_simpson."