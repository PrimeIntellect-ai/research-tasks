# test_final_state.py

import os
import json
import ast
import pytest

def test_deploy_report_generated_correctly():
    report_path = "/home/user/release_prep/deploy_report.json"
    assert os.path.isfile(report_path), f"Deployment report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    assert "status" in data, "Key 'status' missing from deploy_report.json"
    assert data["status"] == "success", f"Expected status 'success', got {data['status']}"

    assert "processed_metrics" in data, "Key 'processed_metrics' missing from deploy_report.json"
    metrics = data["processed_metrics"]

    # Expected logic: 
    # original = [10.5, 20.1, 5.0, 8.2]
    # factor = 2.5
    # appended = original + [original[0] * factor]
    # result = [x * factor for x in appended]

    original = [10.5, 20.1, 5.0, 8.2]
    factor = 2.5
    appended = original + [original[0] * factor]
    expected = [x * factor for x in appended]

    assert len(metrics) == len(expected), f"Expected {len(expected)} metrics, got {len(metrics)}"

    for m, e in zip(metrics, expected):
        assert abs(m - e) < 1e-5, f"Mismatch in processed metrics: expected {e}, got {m}"

def test_test_runner_hypothesis_test():
    test_runner_path = "/home/user/release_prep/test_runner.py"
    assert os.path.isfile(test_runner_path), f"Test runner not found at {test_runner_path}"

    with open(test_runner_path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "The 'hypothesis' library is not imported or used in test_runner.py"
    assert "test_scale_property" in content, "The function 'test_scale_property' is missing in test_runner.py"
    assert "@given" in content, "The '@given' decorator from hypothesis is missing in test_runner.py"

def test_test_runner_import_order_fixed():
    test_runner_path = "/home/user/release_prep/test_runner.py"
    assert os.path.isfile(test_runner_path), f"Test runner not found at {test_runner_path}"

    with open(test_runner_path, "r") as f:
        content = f.read()

    idx_ci_logger = content.find("ci_logger.init_logger()")
    idx_rust_ext = content.find("import rust_ext")

    if idx_ci_logger != -1 and idx_rust_ext != -1:
        assert idx_rust_ext < idx_ci_logger, "Import order bug not fixed: rust_ext must be imported before ci_logger.init_logger() is called."

def test_rust_borrow_checker_fixed():
    lib_rs_path = "/home/user/release_prep/rust_ext/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"Rust source not found at {lib_rs_path}"

    with open(lib_rs_path, "r") as f:
        content = f.read()

    # The bug was `let first = &values[0]; values.push(*first * factor);`
    # A valid fix usually involves copying or cloning, e.g., `let first = values[0];`
    assert "let first = &values[0];\n    values.push(*first * factor);" not in content, "The borrow checker bug in lib.rs is still present."