# test_final_state.py

import os
import math
import pytest

def test_scripts_exist_and_executable():
    """Verify that the shell scripts exist and are executable."""
    ode_solver = "/home/user/ode_solver.sh"
    pipeline = "/home/user/pipeline.sh"

    assert os.path.isfile(ode_solver), f"Missing script: {ode_solver}"
    assert os.access(ode_solver, os.X_OK), f"Script is not executable: {ode_solver}"

    assert os.path.isfile(pipeline), f"Missing script: {pipeline}"
    assert os.access(pipeline, os.X_OK), f"Script is not executable: {pipeline}"

def test_data_directory_and_csv_files():
    """Verify that the data directory and the 5 CSV files exist with the correct header."""
    data_dir = "/home/user/data"
    assert os.path.isdir(data_dir), f"Data directory missing: {data_dir}"

    expected_dts = ["2.0", "1.0", "0.5", "0.1", "0.01"]

    for dt in expected_dts:
        file_path = os.path.join(data_dir, f"dataset_dt_{dt}.csv")
        assert os.path.isfile(file_path), f"Missing dataset file: {file_path}"

        with open(file_path, "r") as f:
            lines = f.readlines()

        assert len(lines) > 1, f"Dataset file {file_path} is empty or missing data rows."
        header = lines[0].strip()
        assert header == "t,y_num,y_exact,abs_error", f"Incorrect CSV header in {file_path}. Found: {header}"

def test_convergence_log():
    """Verify the convergence log format and numerical accuracy."""
    log_file = "/home/user/convergence_log.txt"
    assert os.path.isfile(log_file), f"Missing convergence log: {log_file}"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 6, f"Convergence log has insufficient lines. Expected at least 6 (header + 5 values)."
    assert lines[0] == "dt,final_abs_error", f"Incorrect header in convergence log. Found: {lines[0]}"

    # Calculate exact expected errors
    # Exact solution at t=20: 1000 * exp(-0.2 * 20) = 1000 * exp(-4)
    exact_y = 1000.0 * math.exp(-4.0)

    expected_errors = {}
    for dt in [2.0, 1.0, 0.5, 0.1, 0.01]:
        steps = int(20.0 / dt)
        y_num = 1000.0 * ((1.0 - 0.2 * dt) ** steps)
        expected_errors[str(dt)] = abs(y_num - exact_y)

    log_data = {}
    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) == 2:
            dt_str, err_str = parts
            try:
                log_data[dt_str] = float(err_str)
            except ValueError:
                pass

    for dt_str, expected_err in expected_errors.items():
        assert dt_str in log_data, f"Missing dt={dt_str} in convergence log."
        actual_err = log_data[dt_str]
        assert abs(actual_err - expected_err) < 0.05, (
            f"Numerical error mismatch for dt={dt_str}. "
            f"Expected approx {expected_err:.5f}, got {actual_err:.5f}"
        )