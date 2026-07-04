# test_final_state.py

import os
import json
import stat
import math
import pytest

def test_fix_patch_exists_and_contains_free():
    patch_path = '/home/user/api_backend/fix.patch'
    assert os.path.isfile(patch_path), f"Patch file {patch_path} is missing."

    with open(patch_path, 'r') as f:
        content = f.read()

    assert "free" in content, "The patch file does not appear to add a free() call."
    assert "+" in content and "-" in content, "The patch file does not look like a unified diff."

def test_process_data_binary_exists_and_executable():
    bin_path = '/home/user/api_backend/process_data'
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Compiled binary {bin_path} is not executable."

def test_integration_script_exists_and_executable():
    script_path = '/home/user/test_integration.sh'
    assert os.path.isfile(script_path), f"Integration script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Integration script {script_path} is not executable."

def test_integration_report_json():
    report_path = '/home/user/integration_report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert "l2_norm_from_api" in data, "Key 'l2_norm_from_api' missing from report."
    assert "l1_norm_from_bash" in data, "Key 'l1_norm_from_bash' missing from report."

    l2_norm = float(data["l2_norm_from_api"])
    l1_norm = float(data["l1_norm_from_bash"])

    # Calculate expected values from input_data.txt
    input_path = '/home/user/input_data.txt'
    assert os.path.isfile(input_path), f"Input file {input_path} is missing."

    with open(input_path, 'r') as f:
        numbers = [float(line.strip()) for line in f if line.strip()]

    expected_l1 = sum(abs(x) for x in numbers)
    expected_l2 = math.sqrt(sum(x*x for x in numbers))

    assert math.isclose(l1_norm, expected_l1, rel_tol=1e-3), f"Expected L1 norm ~{expected_l1:.4f}, got {l1_norm}"
    assert math.isclose(l2_norm, expected_l2, rel_tol=1e-3), f"Expected L2 norm ~{expected_l2:.4f}, got {l2_norm}"