# test_final_state.py

import os
import subprocess
import pytest

def test_diagnostic_report_exists():
    report_path = "/home/user/diagnostic_report.txt"
    assert os.path.isfile(report_path), f"{report_path} is missing."
    with open(report_path, 'r') as f:
        lines = f.readlines()
    assert len(lines) >= 2, f"{report_path} must contain at least two lines."

def test_config_acl_resolved():
    config_path = "/home/user/config.json"
    assert os.path.isfile(config_path), f"{config_path} is missing."
    result = subprocess.run(['getfacl', config_path], capture_output=True, text=True)
    assert "user:user:---" not in result.stdout, f"Blocking ACL entry 'user:user:---' is still present on {config_path}."
    assert os.access(config_path, os.R_OK), f"{config_path} is still not readable by the current user."

def test_port_5901_listening():
    result = subprocess.run(['ss', '-tln'], capture_output=True, text=True)
    assert ":5901" in result.stdout, "No service is listening on port 5901. The Expect script may not be running or failed to establish the tunnel."

def test_c_code_and_binary_updated():
    src_path = "/home/user/src/vnc_bridge.c"
    bin_path = "/home/user/bin/vnc_bridge"

    assert os.path.isfile(src_path), f"{src_path} is missing."
    with open(src_path, 'r') as f:
        content = f.read()
    assert "5901" in content, f"The C source code {src_path} does not contain the updated port 5901."

    assert os.path.isfile(bin_path), f"{bin_path} is missing. Did you recompile the C code?"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def test_service_status_log():
    log_path = "/home/user/service_status.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Ensure you ran /home/user/run_bridge.sh."
    with open(log_path, 'r') as f:
        content = f.read()
    assert "Service Started." in content, f"{log_path} does not contain 'Service Started.'. The service is still failing."