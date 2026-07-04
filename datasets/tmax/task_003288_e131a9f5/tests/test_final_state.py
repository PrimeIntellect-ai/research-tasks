# test_final_state.py

import os
import re

def test_bashrc_contains_export():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    match = re.search(r'export\s+QEMU_MONITOR_SOCKET\s*=\s*[\'"]?/home/user/qemu-monitor\.sock[\'"]?', content)
    assert match is not None, f"Could not find 'export QEMU_MONITOR_SOCKET=/home/user/qemu-monitor.sock' in {bashrc_path}."

def test_check_uptime_script_exists_and_valid():
    script_path = "/home/user/check_uptime.py"
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "pexpect" in content, f"The script {script_path} does not seem to use 'pexpect'."
    assert "QEMU_MONITOR_SOCKET" in content, f"The script {script_path} does not read the 'QEMU_MONITOR_SOCKET' environment variable."

def test_uptime_report_content():
    report_path = "/home/user/uptime_report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist. Did you run your script?"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "STATUS: OK - Uptime: 1337 days, 04:20:00"
    assert content == expected, f"Expected report content '{expected}', but got '{content}'."