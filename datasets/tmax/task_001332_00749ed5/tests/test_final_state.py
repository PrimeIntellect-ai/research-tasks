# test_final_state.py

import os
import pytest

def test_integrator_fixed():
    path = "/app/vendored/pydynsim-1.2.0/pydynsim/integrator.py"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "(tolerance / error)**0.5" in content, "The integrator.py does not contain the expected fixed step-size adaptation logic."
    assert "(error / tolerance)**0.5" not in content, "The integrator.py still contains the buggy step-size adaptation logic."

def test_analyze_script_exists():
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"Missing script: {path}"

def test_frequency_output():
    path = "/home/user/frequency.txt"
    assert os.path.isfile(path), f"Missing output file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"File {path} is empty."

    try:
        agent_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {path} as a float. Content: '{content}'")

    target_val = 15.625
    error = abs(agent_val - target_val)

    assert error <= 0.5, f"Calculated frequency {agent_val} is too far from the target {target_val}. Error {error} > 0.5."