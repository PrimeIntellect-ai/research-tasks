# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/orchestrate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_run_script():
    script_path = "/home/user/orchestrate.sh"
    # Run the script to generate the outputs
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_pi_estimate():
    pi_file = "/home/user/data/pi_estimate.txt"
    assert os.path.isfile(pi_file), f"File {pi_file} was not created."
    with open(pi_file, "r") as f:
        content = f.read().strip()
    try:
        pi_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse pi estimate as float: {content}")

    assert 3.0 <= pi_val <= 3.3, f"Pi estimate {pi_val} is not within expected range for Pi (3.0 - 3.3)."

def test_final_report_generated_and_parameters_injected():
    report_file = "/home/user/data/final_report.ipynb"
    assert os.path.isfile(report_file), f"File {report_file} was not created."

    with open(report_file, "r") as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_file} is not a valid JSON/Jupyter Notebook.")

    injected_params = {}
    for cell in nb.get("cells", []):
        tags = cell.get("metadata", {}).get("tags", [])
        if "injected-parameters" in tags:
            source = "".join(cell.get("source", []))
            for line in source.split("\n"):
                if "=" in line and not line.strip().startswith("#"):
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    injected_params[key] = val

    assert "ca_count" in injected_params, "ca_count parameter not found in the injected parameters cell."
    assert injected_params["ca_count"] == "2", f"Expected ca_count=2 based on the PDB file, got {injected_params['ca_count']}."

    assert "pi_estimate" in injected_params, "pi_estimate parameter not found in the injected parameters cell."
    try:
        pi_est = float(injected_params["pi_estimate"])
        assert 3.0 <= pi_est <= 3.3, f"Injected pi_estimate {pi_est} is not within expected range."
    except ValueError:
        pytest.fail(f"Could not parse injected pi_estimate as float: {injected_params['pi_estimate']}")