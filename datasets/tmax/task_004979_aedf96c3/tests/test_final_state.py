# test_final_state.py

import os
import json
import stat

def test_profiler_go_exists():
    """Verify that the Go program exists."""
    assert os.path.isfile("/home/user/profiler.go"), "/home/user/profiler.go does not exist."

def test_run_pipeline_sh_exists_and_executable():
    """Verify that the shell script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_profile_results_json():
    """Verify the contents of the generated JSON file."""
    json_path = "/home/user/profile_results.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist. Did you run the pipeline?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert "integral" in data, "JSON missing 'integral' key."
    assert "derivative" in data, "JSON missing 'derivative' key."

    # Values based on Go's math/rand with seed 12345 and N=1,000,000
    expected_integral = 5365.1053
    expected_derivative = 0.8982

    assert isinstance(data["integral"], (int, float)), "'integral' must be a number."
    assert isinstance(data["derivative"], (int, float)), "'derivative' must be a number."

    assert abs(data["integral"] - expected_integral) < 1e-4, \
        f"Expected integral to be approx {expected_integral}, got {data['integral']}"

    assert abs(data["derivative"] - expected_derivative) < 1e-4, \
        f"Expected derivative to be approx {expected_derivative}, got {data['derivative']}"