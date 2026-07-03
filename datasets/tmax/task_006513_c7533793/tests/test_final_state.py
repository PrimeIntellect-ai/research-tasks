# test_final_state.py

import os
import json
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = "/home/user/uptime_monitor/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lpthread" in content, "Makefile does not contain the fixed linker flag '-lpthread'"
    assert "-lpthred" not in content, "Makefile still contains the typo '-lpthred'"

def test_libmetrics_so_built():
    so_path = "/home/user/uptime_monitor/libmetrics.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built"

def test_agent_execution_no_deadlock():
    agent_path = "/home/user/uptime_monitor/agent.py"
    assert os.path.isfile(agent_path), f"Agent script {agent_path} is missing"

    try:
        result = subprocess.run(
            ["python3", agent_path],
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Agent script timed out after 10 seconds, indicating the deadlock is not fixed.")

    assert result.returncode == 0, f"Agent script failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert "Successfully completed all monitoring queries." in result.stdout, "Agent script did not output the expected success message."

def test_resolution_json():
    json_path = "/home/user/resolution.json"
    assert os.path.isfile(json_path), f"Resolution file {json_path} is missing"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON")

    assert "linker_error_fixed" in data, "Missing 'linker_error_fixed' in resolution.json"
    assert data["linker_error_fixed"] is True, "'linker_error_fixed' must be true"

    assert "deadlocked_functions" in data, "Missing 'deadlocked_functions' in resolution.json"
    expected_functions = ["get_cpu_metrics", "get_mem_metrics"]
    assert data["deadlocked_functions"] == expected_functions, f"'deadlocked_functions' must be exactly {expected_functions}"

    assert "fix_strategy" in data, "Missing 'fix_strategy' in resolution.json"
    assert isinstance(data["fix_strategy"], str) and len(data["fix_strategy"]) > 0, "'fix_strategy' must be a non-empty string"