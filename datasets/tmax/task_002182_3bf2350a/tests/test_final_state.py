# test_final_state.py

import os
import pytest

def test_orchestrate_script_exists_and_executable():
    """Test that orchestrate.sh exists and is executable."""
    script_path = "/home/user/orchestrate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_startup_order_log():
    """Test that startup_order.log contains the correct topological sort."""
    log_path = "/home/user/startup_order.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    expected_order = [
        "ConfigService",
        "DatabaseService",
        "CacheService",
        "AuthService",
        "GatewayService"
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert lines == expected_order, f"Expected startup order {expected_order}, but got {lines}."

def test_valgrind_log_exists():
    """Test that valgrind_auth.log exists and contains valgrind output."""
    log_path = "/home/user/valgrind_auth.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Memcheck" in content or "valgrind" in content.lower() or "definitely lost" in content, \
        f"{log_path} does not appear to contain valid valgrind output."

def test_leak_report():
    """Test that leak_report.txt contains exactly the leaked bytes."""
    report_path = "/home/user/leak_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "4096", f"Expected leak_report.txt to contain '4096', but got '{content}'."