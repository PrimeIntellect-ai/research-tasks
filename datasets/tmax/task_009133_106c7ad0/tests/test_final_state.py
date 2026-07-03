# test_final_state.py

import os
import stat
import base64
import re
import pytest

def test_block_sh_content():
    block_sh_path = "/home/user/block.sh"
    assert os.path.isfile(block_sh_path), f"File {block_sh_path} does not exist."

    # Recompute expected IPs from the log file
    log_path = "/home/user/service.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    malicious_ips = set()
    with open(log_path, "r") as f:
        for line in f:
            match = re.search(r'payload=([A-Za-z0-9+/=]+)', line)
            if match:
                b64_payload = match.group(1)
                try:
                    # Pad the base64 string if necessary
                    b64_payload += "=" * ((4 - len(b64_payload) % 4) % 4)
                    decoded = base64.b64decode(b64_payload).decode('utf-8')

                    if 'wget' in decoded:
                        ip_match = re.search(r'wget\s+http://([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', decoded)
                        if ip_match:
                            malicious_ips.add(ip_match.group(1))
                    elif 'ncat' in decoded:
                        ip_match = re.search(r'ncat\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', decoded)
                        if ip_match:
                            malicious_ips.add(ip_match.group(1))
                except Exception:
                    pass

    sorted_ips = sorted(list(malicious_ips))
    expected_lines = [f"iptables -A INPUT -s {ip} -j DROP" for ip in sorted_ips]

    with open(block_sh_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {block_sh_path} do not match expected firewall rules. Expected: {expected_lines}, Got: {actual_lines}"

def test_vuln_files_txt_content():
    vuln_files_path = "/home/user/vuln_files.txt"
    assert os.path.isfile(vuln_files_path), f"File {vuln_files_path} does not exist."

    suspicious_dir = "/home/user/suspicious_dir"
    assert os.path.isdir(suspicious_dir), f"Directory {suspicious_dir} is missing."

    # Recompute expected vulnerable files
    expected_vuln_files = []
    for filename in os.listdir(suspicious_dir):
        filepath = os.path.join(suspicious_dir, filename)
        if os.path.isfile(filepath):
            st = os.stat(filepath)
            mode = st.st_mode
            is_suid = bool(mode & stat.S_ISUID)
            is_world_writable = bool(mode & stat.S_IWOTH)

            if is_suid or is_world_writable:
                expected_vuln_files.append(filename)

    expected_vuln_files.sort()

    with open(vuln_files_path, "r") as f:
        actual_files = [line.strip() for line in f if line.strip()]

    assert actual_files == expected_vuln_files, f"Contents of {vuln_files_path} do not match expected vulnerable files. Expected: {expected_vuln_files}, Got: {actual_files}"

def test_original_files_unmodified():
    # Check that service.log hasn't been modified (basic line count/content check)
    log_path = "/home/user/service.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."
    with open(log_path, "r") as f:
        lines = f.readlines()
    assert len(lines) == 6, f"File {log_path} seems to have been modified (incorrect number of lines)."
    assert "ZWNobyAiaGVsbG8i" in lines[0], f"File {log_path} seems to have been modified."

    # Check that suspicious_dir contents haven't been modified
    files_to_check = {
        "clean_file.txt": 0o644,
        "backdoor_bin": 0o4755,
        "config.json": 0o777,
        "script.sh": 0o755,
        "suid_script": 0o4644
    }

    for filename, expected_mode in files_to_check.items():
        filepath = f"/home/user/suspicious_dir/{filename}"
        assert os.path.isfile(filepath), f"Original file {filepath} was deleted or moved."
        st = os.stat(filepath)
        actual_mode = stat.S_IMODE(st.st_mode)
        assert actual_mode == expected_mode, f"Permissions of {filepath} were modified. Expected {oct(expected_mode)}, got {oct(actual_mode)}"