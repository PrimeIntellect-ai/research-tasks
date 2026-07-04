# test_final_state.py

import os
import re

def test_nginx_service_after():
    path = "/home/user/.config/systemd/user/nginx.service"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()

    # Check if After=api.service is present
    assert re.search(r"^After\s*=\s*api\.service", content, re.MULTILINE), \
        f"Missing or incorrect 'After=api.service' directive in {path}"

def test_api_service_environment_file():
    path = "/home/user/.config/systemd/user/api.service"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()

    # Check if EnvironmentFile=/home/user/app.env is present
    assert re.search(r"^EnvironmentFile\s*=\s*/home/user/app\.env", content, re.MULTILINE), \
        f"Missing or incorrect 'EnvironmentFile=/home/user/app.env' directive in {path}"

def test_nginx_conf_proxy_pass():
    path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()

    # Check if proxy_pass points to port 8000
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:8000\s*;", content), \
        f"proxy_pass is not correctly set to http://127.0.0.1:8000; in {path}"

def test_app_public_symlink():
    link_path = "/home/user/app/public"
    target_path = "/home/user/shared_public"

    assert os.path.islink(link_path), f"Path {link_path} is not a symbolic link"

    actual_target = os.readlink(link_path)
    assert actual_target == target_path, \
        f"Symlink {link_path} points to {actual_target} instead of {target_path}"

def test_502_ips_extracted():
    log_path = "/home/user/logs/nginx_access.log"
    output_path = "/home/user/502_ips.txt"

    assert os.path.isfile(log_path), f"Original log file missing: {log_path}"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    # Derive expected IPs from the log file
    expected_ips = set()
    with open(log_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) > 8 and parts[8] == "502":
                expected_ips.add(parts[0])

    # Read actual IPs from the output file
    actual_ips = set()
    with open(output_path, "r") as f:
        for line in f:
            ip = line.strip()
            if ip:
                actual_ips.add(ip)

    assert actual_ips == expected_ips, \
        f"Extracted IPs {actual_ips} do not match the expected 502 IPs {expected_ips}"