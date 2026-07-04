# test_final_state.py

import os
import json
import pytest

def test_metrics_thresholds():
    """
    Reads the metrics.json file produced by the regression test and checks
    that the metrics meet the required thresholds.
    """
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), f"Metrics file not found at {metrics_path}. Did you run the regression test?"

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {metrics_path} as valid JSON.")

    assert "reconstruction_error" in metrics, "Metric 'reconstruction_error' is missing from metrics.json"
    assert "execution_time" in metrics, "Metric 'execution_time' is missing from metrics.json"

    recon_err = float(metrics["reconstruction_error"])
    exec_time = float(metrics["execution_time"])

    recon_threshold = 1e-7
    exec_threshold = 1.5

    assert recon_err <= recon_threshold, (
        f"Reconstruction error {recon_err} is too high! "
        f"Threshold is <= {recon_threshold}. The algorithm precision has not been properly restored."
    )

    assert exec_time <= exec_threshold, (
        f"Execution time {exec_time}s is too high! "
        f"Threshold is <= {exec_threshold}s. The build optimization has not been properly restored."
    )

def test_installed_artifacts():
    """
    Checks that the library and headers were installed to /home/user/local/
    and the compiled executable is at /home/user/run_test.
    """
    header_path = "/home/user/local/include/svd.h"
    assert os.path.exists(header_path), f"Header file not installed at {header_path}"

    lib_path_1 = "/home/user/local/lib/libsvd_fast.so"
    lib_path_2 = "/home/user/local/lib64/libsvd_fast.so"
    assert os.path.exists(lib_path_1) or os.path.exists(lib_path_2), (
        "Shared library libsvd_fast.so not found in /home/user/local/lib/ or /home/user/local/lib64/"
    )

    executable_path = "/home/user/run_test"
    assert os.path.exists(executable_path), f"Compiled test executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"