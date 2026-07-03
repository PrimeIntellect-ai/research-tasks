# test_final_state.py

import os
import pytest

def test_fixed_averages_file_exists():
    assert os.path.isfile('/home/user/fixed_epoch_averages.txt'), "The output file /home/user/fixed_epoch_averages.txt is missing."

def test_fixed_averages_content():
    with open('/home/user/fixed_epoch_averages.txt', 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 100, f"Expected 100 lines in fixed_epoch_averages.txt, got {len(lines)}."

    loss = 1.0
    for i, line in enumerate(lines):
        epoch = i + 1
        loss *= 0.95
        expected_str = f"Epoch {epoch}: {loss:.6f}"
        assert line == expected_str, f"Mismatch at epoch {epoch}: expected '{expected_str}', got '{line}'"

def test_aggregate_script_exists_and_executable():
    script_path = '/home/user/aggregate.sh'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."