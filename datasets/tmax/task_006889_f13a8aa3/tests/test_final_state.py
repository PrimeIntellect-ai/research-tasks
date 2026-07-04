# test_final_state.py
import os
import subprocess
import pytest

def test_send_alert_exp_exists_and_executable():
    path = "/home/user/send_alert.exp"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_log_monitor_binary_exists():
    path = "/home/user/log_monitor/target/release/log_monitor"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_config_fw_sh_idempotent():
    path = "/home/user/config_fw.sh"
    assert os.path.exists(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

    conf_path = "/home/user/firewall.conf"

    # Run the script 3 times to test idempotency
    for _ in range(3):
        result = subprocess.run([path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    assert os.path.exists(conf_path), f"{conf_path} was not created by the script"

    with open(conf_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    forward_rule = "FORWARD PORT 8080 TO 9090"
    block_rule = "BLOCK PORT 22"

    assert lines.count(forward_rule) == 1, f"Expected exactly one '{forward_rule}' in {conf_path}, found {lines.count(forward_rule)}"
    assert lines.count(block_rule) == 1, f"Expected exactly one '{block_rule}' in {conf_path}, found {lines.count(block_rule)}"

def test_log_monitor_integration():
    binary_path = "/home/user/log_monitor/target/release/log_monitor"
    log_path = "/home/user/test_system.log"
    outbox_path = "/home/user/outbox.txt"

    # Clean up any existing outbox to ensure a fresh test
    if os.path.exists(outbox_path):
        os.remove(outbox_path)

    result = subprocess.run([binary_path, log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Rust binary failed with error: {result.stderr}"

    assert os.path.exists(outbox_path), f"{outbox_path} was not created after running log_monitor"

    with open(outbox_path, "r") as f:
        content = f.read()

    expected_content = (
        "TO: oncall@local.domain\n"
        "SUBJECT: Critical System Alert\n"
        "BODY: [CRITICAL] Database connection lost\n"
        "---\n"
        "TO: oncall@local.domain\n"
        "SUBJECT: Critical System Alert\n"
        "BODY: [CRITICAL] OOM Killer invoked\n"
        "---\n"
    )

    assert content == expected_content, f"Outbox content did not match expected.\nExpected:\n{expected_content}\nGot:\n{content}"