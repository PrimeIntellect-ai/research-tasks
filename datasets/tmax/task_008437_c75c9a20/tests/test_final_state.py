# test_final_state.py

import os
import subprocess
import pytest

def test_analyze_script_exists_and_executable():
    """Check that the analyze.sh script exists and is executable."""
    script_path = '/home/user/analyze.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_run_analyze_script():
    """Run the analyze.sh script to generate the outputs."""
    script_path = '/home/user/analyze.sh'
    if not os.path.exists(script_path):
        pytest.skip(f"Script {script_path} does not exist.")

    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}\n{result.stdout}"

def test_peak_freq_output():
    """Check that the peak frequency output file has the correct value."""
    file_path = '/home/user/peak_freq.txt'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == '150', f"Expected '150' in {file_path}, but got '{content}'."

def test_zscore_output():
    """Check that the z-score output file has the correct value."""
    file_path = '/home/user/zscore.txt'
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == '22.51', f"Expected '22.51' in {file_path}, but got '{content}'."