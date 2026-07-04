# test_final_state.py

import os
import re
import subprocess
import pytest

def test_calibration_key_restored():
    config_path = '/home/user/config.env'
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing."

    with open(config_path, 'r') as f:
        config_content = f.read()

    assert "0x9A4F2B1C" in config_content.upper(), "Calibration key 0x9A4F2B1C not correctly restored in config.env."

def test_dependency_conflict_resolved():
    makefile_path = '/app/services/backend_c/Makefile'
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        makefile_content = f.read()

    assert 'lmatrix_v2' in makefile_content, "Makefile does not link against the correct libmatrix_v2.so."
    assert 'lmatrix_v1' not in makefile_content, "Makefile still links against the buggy libmatrix_v1.so."

def test_crash_input_saved():
    crash_path = '/home/user/crash_input.hex'
    assert os.path.isfile(crash_path), f"Crash input file {crash_path} is missing."

    with open(crash_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, "Crash input file is empty."
    # Basic hex check
    try:
        bytes.fromhex(content.replace('\\x', '').replace('0x', '').replace('\n', '').replace(' ', ''))
    except ValueError:
        pytest.fail("Crash input file does not contain valid hex-encoded data.")

def test_mse_metric_threshold():
    script_path = '/app/evaluate_mse.py'
    assert os.path.isfile(script_path), f"Evaluation script {script_path} is missing."

    result = subprocess.run(['python3', script_path], capture_output=True, text=True)

    assert result.returncode == 0, f"evaluate_mse.py failed to run. Stderr: {result.stderr}"

    match = re.search(r'FINAL_MSE:\s*([0-9.]+)', result.stdout)
    assert match is not None, f"Could not find FINAL_MSE in output. Stdout: {result.stdout}"

    mse_value = float(match.group(1))
    threshold = 0.001

    assert mse_value < threshold, f"Metric threshold failed: MSE {mse_value} is not < {threshold}"