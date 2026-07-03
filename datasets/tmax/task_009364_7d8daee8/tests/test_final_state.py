# test_final_state.py

import os
import sys
import pytest
import importlib.util

def test_worker_fixed():
    worker_path = "/home/user/worker.py"
    assert os.path.isfile(worker_path), f"File {worker_path} does not exist"

    spec = importlib.util.spec_from_file_location("worker", worker_path)
    worker = importlib.util.module_from_spec(spec)
    sys.modules["worker"] = worker
    spec.loader.exec_module(worker)

    assert hasattr(worker, "calculate_weight"), "worker.py is missing calculate_weight function"

    try:
        res_neg = worker.calculate_weight(-3)
        assert res_neg == 0, f"Expected calculate_weight(-3) to return 0, but got {res_neg}"

        res_zero = worker.calculate_weight(0)
        assert res_zero == 0, f"Expected calculate_weight(0) to return 0, but got {res_zero}"

        res_pos = worker.calculate_weight(5)
        assert res_pos == 8, f"Expected calculate_weight(5) to return 8, but got {res_pos}"
    except RecursionError:
        pytest.fail("calculate_weight raised a RecursionError, meaning the base case for n <= 0 is still missing or incorrect.")

def test_run_after_log_exists():
    path = "/home/user/logs/run_after.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the run_system.py script?"

    with open(path, "r") as f:
        content = f.read()

    assert "TASK_EVENT ID:4 STATUS:SUCCESS RESULT:0" in content, "run_after.log does not contain the expected success event for ID:4"
    assert "TASK_EVENT ID:5 STATUS:SUCCESS RESULT:8" in content, "run_after.log does not contain the expected success event for ID:5"

def test_diagnostic_report_content():
    report_path = "/home/user/diagnostic_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[2023-10-15T08:01:00] TASK_EVENT ID:1 STATUS:QUEUED",
        "[2023-10-15T08:01:30] TASK_EVENT ID:1 STATUS:SUCCESS RESULT:1",
        "[2023-10-15T08:02:00] TASK_EVENT ID:2 STATUS:QUEUED",
        "[2023-10-15T08:02:30] TASK_EVENT ID:2 STATUS:SUCCESS RESULT:2",
        "[2023-10-15T08:03:00] TASK_EVENT ID:3 STATUS:QUEUED",
        "[2023-10-15T08:04:00] TASK_EVENT ID:3 STATUS:FAILED ERROR:RecursionError",
        "[2023-10-15T08:05:00] TASK_EVENT ID:4 STATUS:SUCCESS RESULT:0",
        "[2023-10-15T08:06:00] TASK_EVENT ID:5 STATUS:SUCCESS RESULT:8"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in diagnostic_report.txt, but got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"