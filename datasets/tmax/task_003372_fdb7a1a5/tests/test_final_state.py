# test_final_state.py
import os
import re
import base64
import socket

def test_compromised_ips_file_exists():
    path = "/home/user/compromised_ips.txt"
    assert os.path.isfile(path), f"The output file {path} does not exist. Did you create it?"

def test_compromised_ips_content():
    elf_path = "/home/user/suspicious.elf"
    log_path = "/home/user/access.log"
    out_path = "/home/user/compromised_ips.txt"

    assert os.path.isfile(elf_path), f"Original file {elf_path} is missing."
    assert os.path.isfile(log_path), f"Original file {log_path} is missing."

    # 1. Extract and decode the regex from the binary
    with open(elf_path, "rb") as f:
        elf_data = f.read()

    match = re.search(b"C2_BEACON:\s*([A-Za-z0-9+/=]+)", elf_data)
    assert match is not None, "Could not find C2_BEACON string in the binary."

    b64_string = match.group(1)
    regex_pattern = base64.b64decode(b64_string).decode('utf-8')

    # Compile the regex
    malicious_re = re.compile(regex_pattern)

    # 2. Parse the access log and find matching IPs
    compromised_ips = set()
    with open(log_path, "r") as f:
        for line in f:
            # Standard combined log format: IP is the first token.
            parts = line.split(maxsplit=1)
            if not parts:
                continue
            ip = parts[0]

            # Extract request URI
            # Format usually: ... "GET /path HTTP/1.1" ...
            req_match = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|OPTIONS) ([^"]+) HTTP', line)
            if req_match:
                request_uri = req_match.group(1)
                if malicious_re.search(request_uri):
                    compromised_ips.add(ip)

    # 3. Sort IPs numerically
    def ip_sort_key(ip_str):
        try:
            return socket.inet_aton(ip_str)
        except socket.error:
            return b'\x00\x00\x00\x00'

    expected_ips = sorted(list(compromised_ips), key=ip_sort_key)
    expected_content = "\n".join(expected_ips) + "\n"

    # 4. Read the student's output file
    with open(out_path, "r") as f:
        actual_content = f.read()

    # Normalize newlines for comparison
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {out_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )