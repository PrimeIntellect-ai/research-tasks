# test_final_state.py

import os
import json
import stat
import pytest

def test_run_analysis_script():
    """Test that run_analysis.sh exists and is executable."""
    script_path = "/home/user/run_analysis.sh"
    assert os.path.exists(script_path), f"File {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

def test_sweep_script():
    """Test that sweep.py exists."""
    script_path = "/home/user/sweep.py"
    assert os.path.exists(script_path), f"File {script_path} is missing."

def test_obs_reshaped():
    """Test that obs_reshaped.csv exists and has the correct reshaped content."""
    csv_path = "/home/user/obs_reshaped.csv"
    assert os.path.exists(csv_path), f"File {csv_path} is missing."

    expected_lines = [
        "day,infected",
        "1,10",
        "2,25",
        "3,50",
        "4,80",
        "5,110"
    ]

    with open(csv_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {csv_path} does not match the expected reshaped format."

def test_profile_log():
    """Test that profile.log exists and contains cProfile output."""
    log_path = "/home/user/profile.log"
    assert os.path.exists(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "function calls" in content or "tottime" in content or "ncalls" in content, \
        f"{log_path} does not appear to contain valid cProfile output."

def test_best_params():
    """Test that best_params.json exists, is valid JSON, and contains the correct best parameters."""
    json_path = "/home/user/best_params.json"
    assert os.path.exists(json_path), f"File {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    assert "beta" in data, "Missing 'beta' in best_params.json"
    assert "gamma" in data, "Missing 'gamma' in best_params.json"
    assert "sse" in data, "Missing 'sse' in best_params.json"

    assert data["beta"] == 0.6, f"Expected best beta to be 0.6, got {data['beta']}"
    assert data["gamma"] == 0.2, f"Expected best gamma to be 0.2, got {data['gamma']}"
    assert isinstance(data["sse"], (int, float)), "SSE should be a number"
    assert data["sse"] > 0, "SSE should be a positive number"