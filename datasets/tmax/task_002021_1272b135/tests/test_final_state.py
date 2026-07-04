# test_final_state.py
import os
import pytest

def test_runner_patched():
    path = '/home/user/qa/test_runner.sh'
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, 'r') as f:
        content = f.read()
    assert "<<< END COMPONENT" in content, "test_runner.sh was not patched correctly (missing <<< END COMPONENT)."
    assert "<<< FINISH COMPONENT" not in content, "test_runner.sh still contains <<< FINISH COMPONENT."

def test_raw_benchmark_log_exists():
    path = '/home/user/qa/raw_benchmark.log'
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, 'r') as f:
        content = f.read()
    assert "<<< END COMPONENT" in content, "raw_benchmark.log does not contain the expected markers from the patched runner."

def test_parser_awk_exists():
    path = '/home/user/qa/parser.awk'
    assert os.path.isfile(path), f"{path} is missing."

def test_final_report_correct():
    path = '/home/user/qa/final_report.txt'
    assert os.path.isfile(path), f"{path} is missing."

    expected = [
        "C_Core_TOTAL:15ms",
        "Python_Worker_TOTAL:87ms",
        "Go_Service_TOTAL:33ms"
    ]

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected, f"final_report.txt content is incorrect. Expected {expected}, got {lines}."