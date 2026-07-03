# test_final_state.py

import os
import json
import pytest

def test_integrator_fixed():
    filepath = "/home/user/sim/integrator.cpp"
    assert os.path.isfile(filepath), f"{filepath} does not exist"

    with open(filepath, "r") as f:
        content = f.read()

    assert "TOL / error" in content, "The bug in integrator.cpp was not fixed. Expected 'TOL / error' to be used in the scale calculation."

def test_executable_compiled():
    filepath = "/home/user/sim/build/vdp_sim"
    assert os.path.isfile(filepath), f"Compiled executable {filepath} does not exist. Did you run cmake and make?"
    assert os.access(filepath, os.X_OK), f"File {filepath} is not executable."

def test_notebook_executed():
    filepath = "/home/user/sim/experiment_out.ipynb"
    assert os.path.isfile(filepath), f"Executed notebook {filepath} does not exist. Did you run papermill?"

def test_result_json_stable():
    filepath = "/home/user/sim/result.json"
    assert os.path.isfile(filepath), f"Result file {filepath} does not exist. The notebook may not have executed successfully."

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON.")

    assert data.get("status") == "stable", f"Expected simulation status to be 'stable', but got '{data.get('status')}'. The integration logic might still be incorrect."