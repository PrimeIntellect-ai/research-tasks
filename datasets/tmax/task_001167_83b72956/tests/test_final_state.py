# test_final_state.py

import os
import pytest

def test_agent_fixed_exists_and_executable():
    agent_fixed_path = "/home/user/telemetry_diag/agent_fixed"
    assert os.path.isfile(agent_fixed_path), f"File {agent_fixed_path} does not exist. Did you recompile the agent as 'agent_fixed'?"
    assert os.access(agent_fixed_path, os.X_OK), f"File {agent_fixed_path} is not executable."

def test_diagnostic_report_exists_and_correct():
    report_path = "/home/user/telemetry_diag/diagnostic_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist. Did you run the fixed agent and redirect its output?"

    with open(report_path, "r") as f:
        content = f.read()

    assert "RMS:" in content, "The diagnostic report does not contain the 'RMS:' prefix."

    # The expected RMS is approx 50662.277...
    # We check for 50662 to allow for different decimal formatting.
    assert "50662" in content, f"The calculated RMS value is incorrect or missing. Expected a value around 50662, but got:\n{content}"