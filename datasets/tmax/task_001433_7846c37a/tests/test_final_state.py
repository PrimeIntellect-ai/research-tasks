# test_final_state.py
import os
import json
import pytest

def test_diagnostics_file_exists():
    assert os.path.isfile('/home/user/app/diagnostics.json'), "The diagnostics.json file was not generated. Did you send the SIGUSR1 signal to the service?"

def test_diagnostics_content():
    diagnostics_path = '/home/user/app/diagnostics.json'
    assert os.path.isfile(diagnostics_path), f"File missing: {diagnostics_path}"

    with open(diagnostics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("diagnostics.json does not contain valid JSON.")

    assert 'active_tasks' in data, "diagnostics.json is missing the 'active_tasks' key."
    assert data['active_tasks'] == 0, f"Task leak detected: {data['active_tasks']} active tasks remaining. Expected 0."

    assert 'ema' in data, "diagnostics.json is missing the 'ema' key."

    # Deriving the expected EMA based on the client.py workload
    expected_ema = 0.0
    alpha = 0.5
    values = [10, 20, 50, 80, 100]

    for v in values:
        expected_ema = (v * alpha) + (expected_ema * (1 - alpha))

    actual_ema = data['ema']
    assert abs(actual_ema - expected_ema) < 0.001, f"Incorrect EMA calculation. Expected around {expected_ema}, but got {actual_ema}."