# test_final_state.py
import os
import pytest

def test_calculated_sla_accuracy():
    target_file = "/home/user/calculated_sla.txt"
    assert os.path.isfile(target_file), f"Output file {target_file} does not exist."

    with open(target_file, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {target_file}.")

    truth = 99.999142
    error = abs(val - truth)
    threshold = 1e-6

    assert error < threshold, f"Calculated SLA {val} is not accurate enough. Error {error} >= threshold {threshold}."