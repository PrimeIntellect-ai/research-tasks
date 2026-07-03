# test_final_state.py
import os
import re
import pytest

def test_launcher_sh_start_order():
    path = "/home/user/launcher.sh"
    assert os.path.exists(path), f"{path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    # Find the START ORDER section or just the last occurrences
    # It's safer to find the last occurrence of the calls.
    # The definitions have "() {" so we should look for lines that do not have "() {"
    lines = content.splitlines()

    proxy_idx = -1
    capacity_idx = -1

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("start_proxy") and "()" not in line:
            proxy_idx = i
        elif line.startswith("start_capacity_tool") and "()" not in line:
            capacity_idx = i

    assert proxy_idx != -1, "start_proxy call not found in launcher.sh"
    assert capacity_idx != -1, "start_capacity_tool call not found in launcher.sh"
    assert proxy_idx < capacity_idx, "start_proxy is not called before start_capacity_tool in launcher.sh"

def test_proxy_conf_content():
    path = "/home/user/proxy.conf"
    assert os.path.exists(path), f"{path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    # Clean up whitespace for easier matching
    cleaned_content = re.sub(r'\s+', ' ', content)

    assert "daemon off;" in cleaned_content, "Missing 'daemon off;' in proxy.conf"
    assert "pid /home/user/nginx.pid;" in cleaned_content, "Missing 'pid /home/user/nginx.pid;' in proxy.conf"
    assert "error_log /home/user/error.log;" in cleaned_content, "Missing 'error_log /home/user/error.log;' in proxy.conf"

    assert re.search(r'listen\s+(?:\*:)?8080;', cleaned_content), "Missing 'listen 8080;' or 'listen *:8080;' in proxy.conf"
    assert re.search(r'proxy_pass\s+http://127\.0\.0\.1:9090;', cleaned_content), "Missing 'proxy_pass http://127.0.0.1:9090;' in proxy.conf"

def test_generate_report_exp_exists_and_content():
    path = "/home/user/generate_report.exp"
    assert os.path.exists(path), f"{path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "spawn" in content, "Expect script does not contain a 'spawn' command"
    assert "/home/user/capacity_cli" in content, "Expect script does not spawn '/home/user/capacity_cli'"

def test_capacity_report_txt_content():
    path = "/home/user/capacity_report.txt"
    assert os.path.exists(path), f"{path} does not exist. The expect script might not have been executed or did not save the output."

    with open(path, "r") as f:
        content = f.read()

    assert "TZ: America/New_York" in content, "Missing or incorrect TZ output in capacity_report.txt"
    assert "LOC: en_US.UTF-8" in content, "Missing or incorrect LOC output in capacity_report.txt"
    assert "USER: sys_planner" in content, "Missing or incorrect USER output in capacity_report.txt"
    assert "GROUP: capacity_admins" in content, "Missing or incorrect GROUP output in capacity_report.txt"
    assert "STATUS: SUCCESS" in content, "Missing STATUS: SUCCESS in capacity_report.txt"