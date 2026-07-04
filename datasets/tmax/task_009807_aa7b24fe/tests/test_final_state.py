# test_final_state.py

import os
import subprocess
import pytest

def test_main_rs_fixed():
    main_rs_path = "/home/user/sim_project/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} is missing"

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "adj[i][j] * 1.5" not in content, "The bug 'adj[i][j] * 1.5' is still present in main.rs"
    assert "deg[i]" in content, "The fix using 'deg[i]' is not present in main.rs"

def test_run_regression_script_exists_and_executable():
    script_path = "/home/user/run_regression.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_regression_script_behavior():
    script_path = "/home/user/run_regression.sh"
    result_path = "/home/user/regression_result.txt"

    # Remove result file if it exists to ensure the script creates it
    if os.path.exists(result_path):
        os.remove(result_path)

    # Run the script
    result = subprocess.run([script_path], cwd="/home/user", capture_output=True)

    assert result.returncode == 0, f"run_regression.sh exited with code {result.returncode}, expected 0"

    assert os.path.isfile(result_path), f"{result_path} was not created by the script"
    with open(result_path, "r") as f:
        result_content = f.read().strip()

    assert result_content == "PASS", f"Expected 'PASS' in {result_path}, got '{result_content}'"

def test_signal_output():
    signal_path = "/home/user/sim_project/signal.txt"
    assert os.path.isfile(signal_path), f"{signal_path} is missing"

    with open(signal_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 100, f"Expected exactly 100 lines in {signal_path}, got {len(lines)}"

    try:
        last_val = float(lines[-1])
    except ValueError:
        pytest.fail(f"Could not parse the last line of {signal_path} as a float")

    assert 0.1 <= last_val <= 0.5, f"Expected last signal value to be between 0.1 and 0.5, got {last_val}"