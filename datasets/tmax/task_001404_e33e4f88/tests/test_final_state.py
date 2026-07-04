# test_final_state.py

import os
import re
import pytest

def test_high_latency_ips():
    """Verify that high_latency.txt contains the correct unique IPs."""
    file_path = "/home/user/high_latency.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = {"192.168.1.11", "192.168.1.12", "192.168.1.15"}
    actual_ips = set(lines)

    assert len(lines) == 3, f"Expected exactly 3 lines in {file_path}, found {len(lines)}."
    assert actual_ips == expected_ips, f"Expected IPs {expected_ips}, but found {actual_ips}."

def test_c_server_files_exist():
    """Verify that the C source and compiled executable exist."""
    source_path = "/home/user/server.c"
    exec_path = "/home/user/server"

    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."
    assert os.path.isfile(exec_path), f"Executable {exec_path} does not exist."
    assert os.access(exec_path, os.X_OK), f"File {exec_path} is not executable."

def test_haproxy_config():
    """Verify HAProxy configuration contains expected bindings and backends."""
    config_path = "/home/user/haproxy.cfg"
    assert os.path.isfile(config_path), f"HAProxy config {config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:9000" in content or "*:9000" in content or "9000" in content, "HAProxy config missing frontend port 9000."
    assert "9001" in content, "HAProxy config missing backend port 9001."
    assert "9002" in content, "HAProxy config missing backend port 9002."

def test_proxy_results_log():
    """Verify proxy_results.log has exactly 4 lines alternating timezones."""
    log_path = "/home/user/proxy_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {log_path}, found {len(lines)}."

    jst_count = 0
    lon_count = 0

    for line in lines:
        if "JST" in line:
            jst_count += 1
        elif "GMT" in line or "BST" in line:
            lon_count += 1
        else:
            pytest.fail(f"Line '{line}' does not contain expected timezone (JST, GMT, or BST).")

    assert jst_count == 2, f"Expected 2 lines with JST, found {jst_count}."
    assert lon_count == 2, f"Expected 2 lines with GMT/BST, found {lon_count}."