# test_final_state.py

import os
import re
import pytest

BASE_DIR = "/home/user/build_metrics"

def get_expected_stats():
    starts = {}
    durations = []
    log_path = os.path.join(BASE_DIR, "build_trace.log")

    if not os.path.exists(log_path):
        return 0, 0

    with open(log_path, "r") as f:
        for line in f:
            if line.startswith("START_TRACE::"):
                parts = line.strip().split("::")
                if len(parts) == 3:
                    starts[parts[1]] = int(parts[2])
            elif line.startswith("END_TRACE::"):
                parts = line.strip().split("::")
                if len(parts) == 3:
                    name = parts[1]
                    end_ts = int(parts[2])
                    if name in starts and name.startswith("mobile_module_"):
                        durations.append(end_ts - starts[name])

    if durations:
        mean = sum(durations) / len(durations)
        variance = sum((x - mean) ** 2 for x in durations) / len(durations)
        return mean, variance
    return 0, 0

def test_fast_parser_c_exists():
    c_file = os.path.join(BASE_DIR, "fast_parser.c")
    assert os.path.isfile(c_file), "fast_parser.c is missing."

def test_makefile_exists_and_configured():
    makefile_path = os.path.join(BASE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), "Makefile is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-O3" in content, "Makefile does not use -O3 optimization."
    assert "stats" in content, "Makefile does not link against stats library."

def test_fast_parser_executable_exists():
    exe_path = os.path.join(BASE_DIR, "fast_parser")
    assert os.path.isfile(exe_path), "fast_parser executable is missing."
    assert os.access(exe_path, os.X_OK), "fast_parser is not executable."

def test_report_txt_content():
    report_path = os.path.join(BASE_DIR, "report.txt")
    assert os.path.isfile(report_path), "report.txt is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"report.txt should have exactly 3 lines, found {len(lines)}."

    expected_mean, expected_variance = get_expected_stats()
    expected_mean_str = f"Mean: {expected_mean:.2f}"
    expected_variance_str = f"Variance: {expected_variance:.2f}"

    assert lines[0] == expected_mean_str, f"Expected '{expected_mean_str}', got '{lines[0]}'"
    assert lines[1] == expected_variance_str, f"Expected '{expected_variance_str}', got '{lines[1]}'"
    assert lines[2] == "Fast Parser was Faster: True", f"Expected 'Fast Parser was Faster: True', got '{lines[2]}'"