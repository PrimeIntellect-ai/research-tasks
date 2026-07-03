# test_final_state.py

import os
import re

def test_script_exists_and_executable():
    script_path = '/home/user/bootstrap_corr.sh'
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_result_file_exists():
    result_path = '/home/user/result.txt'
    assert os.path.exists(result_path), f"Result file missing: {result_path}"
    assert os.path.isfile(result_path), f"Path is not a file: {result_path}"

def test_result_format_and_values():
    result_path = '/home/user/result.txt'
    with open(result_path, 'r') as f:
        text = f.read()

    match = re.search(r'Mean:\s+([0-9\.]+)\nSD:\s+([0-9\.]+)', text.strip())
    assert match is not None, "Output format incorrect. Expected 'Mean: 0.XXXX\\nSD: 0.XXXX'"

    mean_val = float(match.group(1))
    sd_val = float(match.group(2))

    assert 0.9600 <= mean_val <= 0.9999, f"Mean {mean_val} out of expected bounds [0.9600, 0.9999]"
    assert 0.0010 <= sd_val <= 0.0400, f"SD {sd_val} out of expected bounds [0.0010, 0.0400]"