# test_final_state.py

import os
import pytest

def test_recovered_metrics_exists():
    assert os.path.isfile("/home/user/db_recovery/recovered_metrics.txt"), "The file /home/user/db_recovery/recovered_metrics.txt is missing. Did you redirect the output?"

def test_recovered_metrics_content():
    expected_lines = [
        "active_connections=1042",
        "request_rate=500",
        "cpu_load_avg=3.14",
        "memory_usage_bytes=" + "9" * 1000,
        "uptime_seconds=86400"
    ]

    filepath = "/home/user/db_recovery/recovered_metrics.txt"
    with open(filepath, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in recovered_metrics.txt, but got {len(lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, lines)):
        assert expected == actual, f"Mismatch on line {i+1}. Expected '{expected[:50]}...', but got '{actual[:50]}...'."

def test_recover_cpp_fixed():
    filepath = "/home/user/db_recovery/recover.cpp"
    assert os.path.isfile(filepath), "recover.cpp is missing."

    with open(filepath, "r") as f:
        content = f.read()

    # Check that the buggy string constructors were fixed
    assert "std::string key(key_buf);" not in content, "recover.cpp still contains the buggy key string constructor."
    assert "std::string val(val_buf);" not in content, "recover.cpp still contains the buggy val string constructor."