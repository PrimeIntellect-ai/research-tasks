# test_final_state.py

import os
import json
import time
import sys
import importlib.util

def test_anomaly_report_exists_and_valid():
    report_path = "/home/user/anomaly_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} is not valid JSON."

    expected_keys = {"slow_request_id", "anomaly_feature"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, got {set(data.keys())}"

    assert data["slow_request_id"] == "REQ-103", f"Expected slow_request_id to be 'REQ-103', got {data['slow_request_id']}"
    assert data["anomaly_feature"] in {"StdDev", "Variance"}, f"Expected anomaly_feature to be 'StdDev' or 'Variance', got {data['anomaly_feature']}"

def test_math_compute_behavior():
    module_path = "/home/user/math_compute.py"
    assert os.path.isfile(module_path), f"{module_path} does not exist."

    # Dynamically import the module
    spec = importlib.util.spec_from_file_location("math_compute", module_path)
    math_compute = importlib.util.module_from_spec(spec)
    sys.modules["math_compute"] = math_compute
    try:
        spec.loader.exec_module(math_compute)
    except Exception as e:
        assert False, f"Failed to import {module_path}: {e}"

    assert hasattr(math_compute, "normalize_and_compute"), "Function 'normalize_and_compute' is missing from math_compute.py"

    test_data = [5.0, 5.0, 5.0, 5.0, 5.0]
    start_time = time.time()
    try:
        result = math_compute.normalize_and_compute(test_data)
    except Exception as e:
        assert False, f"normalize_and_compute raised an exception: {e}"
    duration = time.time() - start_time

    assert duration < 1.0, f"normalize_and_compute took {duration:.2f}s, which is too long (expected < 1.0s). Did you fix the slow fallback?"
    assert result == [0.0, 0.0, 0.0, 0.0, 0.0], f"Expected output [0.0, 0.0, 0.0, 0.0, 0.0], got {result}"

def test_success_log_exists():
    success_path = "/home/user/success.log"
    assert os.path.isfile(success_path), f"Success log {success_path} does not exist. Did you run the verify.py script?"

    with open(success_path, "r") as f:
        content = f.read().strip()
        assert content == "VERIFICATION_PASSED", f"Expected 'VERIFICATION_PASSED' in {success_path}, got {content}"