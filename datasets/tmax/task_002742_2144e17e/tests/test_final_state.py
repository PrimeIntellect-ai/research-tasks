# test_final_state.py

import os
import json
import subprocess
import pytest

def test_rust_lib_fixed():
    lib_path = "/home/user/engine/src/lib.rs"
    assert os.path.isfile(lib_path), f"{lib_path} is missing."
    with open(lib_path, "r") as f:
        content = f.read()
    assert "into_raw" in content or "as_ptr" not in content, "The Rust bug in lib.rs does not appear to be fixed (still returning a dropped pointer instead of transferring ownership)."

def test_ci_run_script():
    script_path = "/home/user/ci_run.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the script and check exit code
    result = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_benchmark_report():
    report_path = "/home/user/benchmark_report.json"
    assert os.path.isfile(report_path), f"{report_path} was not created."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    assert "match" in data, "JSON missing 'match' key."
    assert data["match"] is True, "'match' key in JSON is not true."

    assert "rust_time" in data, "JSON missing 'rust_time' key."
    assert isinstance(data["rust_time"], (int, float)), "'rust_time' is not a number."

    assert "python_time" in data, "JSON missing 'python_time' key."
    assert isinstance(data["python_time"], (int, float)), "'python_time' is not a number."

def test_api_test_script_exists():
    script_path = "/home/user/api_test.py"
    assert os.path.isfile(script_path), f"{script_path} is missing."