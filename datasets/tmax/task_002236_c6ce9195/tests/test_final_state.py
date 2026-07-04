# test_final_state.py
import os
import subprocess
import zlib
import re
import pytest

CONF_PATH = "/home/user/nginx_ws.conf"
BIN_PATH = "/home/user/runner_id.bin"
C_FILE_PATH = "/home/user/calc_proxy.c"

def test_c_file_exists():
    assert os.path.isfile(C_FILE_PATH), f"C program not found at {C_FILE_PATH}"

def test_nginx_conf_exists():
    assert os.path.isfile(CONF_PATH), f"Nginx configuration file not found at {CONF_PATH}"

def test_nginx_conf_content():
    assert os.path.isfile(BIN_PATH), f"File {BIN_PATH} is missing."
    with open(BIN_PATH, "rb") as f:
        content = f.read()

    expected_crc32 = zlib.crc32(content) & 0xFFFFFFFF

    with open(CONF_PATH, "r") as f:
        conf_content = f.read()

    # Check proxy_pass
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:9090/?\s*;", conf_content, re.IGNORECASE), \
        "proxy_pass to http://127.0.0.1:9090 is missing or incorrect."

    # Check WebSocket Upgrade headers
    assert re.search(r"proxy_set_header\s+Upgrade\s+", conf_content, re.IGNORECASE), \
        "WebSocket Upgrade header configuration is missing."
    assert re.search(r"proxy_set_header\s+Connection\s+", conf_content, re.IGNORECASE), \
        "WebSocket Connection header configuration is missing."

    # Check X-Runner-Checksum header
    checksum_regex = rf"proxy_set_header\s+X-Runner-Checksum\s+[\"']?{expected_crc32}[\"']?\s*;"
    assert re.search(checksum_regex, conf_content, re.IGNORECASE), \
        f"X-Runner-Checksum header with value {expected_crc32} is missing or incorrect."

def test_nginx_conf_validity():
    assert os.path.isfile(CONF_PATH), f"Nginx configuration file not found at {CONF_PATH}"

    result = subprocess.run(
        ["nginx", "-t", "-c", CONF_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Nginx configuration test failed:\n{result.stderr}"