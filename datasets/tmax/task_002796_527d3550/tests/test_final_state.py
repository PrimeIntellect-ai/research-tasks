# test_final_state.py
import os

def test_diagnostic_report():
    report_path = "/home/user/diagnostic_report.txt"
    assert os.path.exists(report_path), f"Diagnostic report {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read()

    assert "FAILING_FILE: /tmp/sim_configs/client_a_config_8821.txt" in content, "FAILING_FILE is incorrect or missing."
    assert "PARAM_INITIAL_POS: 850000" in content, "PARAM_INITIAL_POS is incorrect or missing."
    assert "PARAM_VELOCITY: 4000" in content, "PARAM_VELOCITY is incorrect or missing."
    assert "CORRECTED_RESULT: 997415" in content, "CORRECTED_RESULT is incorrect or missing."

def test_test_regression_c():
    test_file = "/home/user/sim_project/test_regression.c"
    assert os.path.exists(test_file), f"Regression test file {test_file} is missing."

    with open(test_file, "r") as f:
        content = f.read()

    assert "trajectory.h" in content, "test_regression.c does not include trajectory.h."
    assert "calc_step" in content, "test_regression.c does not call calc_step."
    assert "850000" in content, "test_regression.c does not use the correct initial_pos."
    assert "4000" in content, "test_regression.c does not use the correct velocity_factor."

def test_test_runner_executable():
    runner_path = "/home/user/sim_project/test_runner"
    assert os.path.exists(runner_path), f"Compiled test runner {runner_path} is missing."
    assert os.access(runner_path, os.X_OK), f"Compiled test runner {runner_path} is not executable."

def test_trajectory_c_fix():
    traj_file = "/home/user/sim_project/trajectory.c"
    assert os.path.exists(traj_file), f"Source file {traj_file} is missing."

    with open(traj_file, "r") as f:
        content = f.read()

    # Check for a 64-bit cast to prevent overflow
    assert "long long" in content or "int64_t" in content or "long" in content, "trajectory.c does not appear to cast the intermediate calculation to a 64-bit integer."