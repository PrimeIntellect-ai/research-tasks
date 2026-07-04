# test_final_state.py
import os
import struct
import urllib.parse
import pytest

def get_expected_log_data():
    log_path = "/home/user/httpd_access.log"
    if not os.path.exists(log_path):
        return None, None

    attacker_ip = None
    stolen_cookie = None

    with open(log_path, "r") as f:
        for line in f:
            if "redirect=" in line and "c=" in line:
                parts = line.split()
                if not parts:
                    continue
                attacker_ip = parts[0]

                # Extract the URL from the request
                request_str = parts[6] if len(parts) > 6 else ""
                if "?" in request_str:
                    query = request_str.split("?", 1)[1]
                    params = urllib.parse.parse_qs(query, keep_blank_values=True)
                    redirect_url = params.get("redirect", [""])[0]
                    if "?" in redirect_url:
                        redirect_query = redirect_url.split("?", 1)[1]
                        # We parse manually because parse_qs might split on & if present,
                        # but the task implies extracting the 'c' parameter value.
                        for param in redirect_query.split("&"):
                            if param.startswith("c="):
                                stolen_cookie = param[2:]
                                break
    return attacker_ip, stolen_cookie

def get_expected_xss_payload():
    bin_path = "/home/user/dropped_data.bin"
    if not os.path.exists(bin_path):
        return None

    record_struct = struct.Struct("<4sI64sB")
    with open(bin_path, "rb") as f:
        while True:
            chunk = f.read(record_struct.size)
            if len(chunk) < record_struct.size:
                break
            magic, ip, payload_bytes, is_xss = record_struct.unpack(chunk)
            if is_xss == 1:
                # Extract null-terminated string
                payload = payload_bytes.split(b'\x00', 1)[0].decode('utf-8', errors='ignore')
                return payload
    return None

def test_stolen_cookie():
    _, expected_cookie = get_expected_log_data()
    assert expected_cookie is not None, "Could not determine expected cookie from log."

    cookie_file = "/home/user/stolen_cookie.txt"
    assert os.path.exists(cookie_file), f"{cookie_file} is missing."

    with open(cookie_file, "r") as f:
        actual_cookie = f.read()

    assert actual_cookie == expected_cookie, f"Expected cookie '{expected_cookie}', got '{actual_cookie}'."

def test_block_script():
    expected_ip, _ = get_expected_log_data()
    assert expected_ip is not None, "Could not determine attacker IP from log."

    block_file = "/home/user/block.sh"
    assert os.path.exists(block_file), f"{block_file} is missing."

    with open(block_file, "r") as f:
        actual_script = f.read().strip()

    expected_script = f"iptables -A INPUT -s {expected_ip} -j DROP"
    assert actual_script == expected_script, f"Expected block script '{expected_script}', got '{actual_script}'."

def test_xss_payload():
    expected_payload = get_expected_xss_payload()
    assert expected_payload is not None, "Could not determine expected XSS payload from binary."

    payload_file = "/home/user/xss_payload.txt"
    assert os.path.exists(payload_file), f"{payload_file} is missing."

    with open(payload_file, "r") as f:
        actual_payload = f.read()

    assert actual_payload == expected_payload, f"Expected XSS payload '{expected_payload}', got '{actual_payload}'."

def test_c_program_exists():
    c_file = "/home/user/parse_bin.c"
    assert os.path.exists(c_file), f"{c_file} is missing."