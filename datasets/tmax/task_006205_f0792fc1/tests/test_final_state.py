# test_final_state.py

import os
import json
import pytest

def compute_golden_values():
    val = 0
    prev_metric = 0.0
    for i in range(1, 10000):
        term = i * i * i
        val += term
        current_metric = 10000.0 / float(val)
        if abs(current_metric - prev_metric) < 1e-7:
            return i, current_metric
        prev_metric = current_metric
    return None, None

def test_config_file_exists_and_correct():
    config_path = '/home/user/.config/app_settings.json'
    assert os.path.exists(config_path), f"Configuration file missing at {config_path}"

    with open(config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} does not contain valid JSON.")

    assert "tolerance" in data, f"'tolerance' key missing in {config_path}"
    assert data["tolerance"] == 1e-7, f"Expected tolerance to be 1e-7, got {data['tolerance']}"

def test_diagnostic_report_correct():
    diagnostic_path = '/home/user/diagnostic.txt'
    assert os.path.exists(diagnostic_path), f"Diagnostic report missing at {diagnostic_path}"

    with open(diagnostic_path, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 2, f"Expected exactly 2 lines in {diagnostic_path}, found {len(lines)}"

    expected_config_path = '/home/user/.config/app_settings.json'
    assert lines[0] == expected_config_path, f"Line 1 expected to be '{expected_config_path}', got '{lines[0]}'"

    golden_iteration, golden_metric = compute_golden_values()
    expected_output = f"Converged at iteration {golden_iteration} to {golden_metric:.8f}"

    assert lines[1] == expected_output, f"Line 2 expected to be '{expected_output}', got '{lines[1]}'"

def test_process_data_fixed():
    script_path = '/home/user/process_data.py'
    assert os.path.exists(script_path), f"Script missing at {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'np.int64' in content, "The script does not appear to use np.int64 to fix the overflow bug."
    assert 'np.int32' not in content, "The script still contains np.int32 which causes the overflow bug."