# test_final_state.py

import os
import json
import urllib.request
import urllib.error

def test_nginx_config_fixed():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://unix:/tmp/qemu_stats.sock;" in content, "The nginx.conf file does not contain the corrected proxy_pass directive."
    assert "qemu-stats.sock" not in content, "The typo in nginx.conf was not completely removed."

def test_check_capacity_script():
    script_path = "/home/user/check_capacity.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()
    assert "curl" in content, "The script does not use curl."
    assert "8080" in content, "The script does not target port 8080."
    assert "capacity_report.txt" in content, "The script does not seem to save to capacity_report.txt."

def test_capacity_report_content():
    report_path = "/home/user/capacity_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist. Did you run the script?"
    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = '{"vms_running": 3, "qemu_cpu_usage": "45%", "qemu_mem_usage": "2GB"}'
    assert content == expected_content, f"The content of {report_path} does not match the expected JSON payload."

def test_services_running_and_reachable():
    # Test if Nginx and the Go API are actually running and wired correctly
    url = "http://127.0.0.1:8080/stats"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()
    except urllib.error.URLError as e:
        assert False, f"Failed to reach the Nginx endpoint at {url}. Is Nginx running? Error: {e}"

    assert status == 200, f"Expected HTTP 200 OK, got {status}."
    expected_content = '{"vms_running": 3, "qemu_cpu_usage": "45%", "qemu_mem_usage": "2GB"}'
    assert body == expected_content, "The endpoint did not return the expected JSON payload. Is the Go API running and proxy configured correctly?"