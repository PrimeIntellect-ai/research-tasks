# test_final_state.py

import os
import stat
import subprocess
import glob
import pytest

def get_expected_ips():
    log_path = '/home/user/access.log'
    if not os.path.exists(log_path):
        return []

    malicious_ips = set()
    with open(log_path, 'r') as f:
        for line in f:
            if 'UNION SELECT' in line:
                parts = line.split()
                if parts:
                    malicious_ips.add(parts[0])

    return sorted(list(malicious_ips))

def get_expected_ports():
    cert_dir = '/home/user/certs'
    expired_ports = []

    for cert_path in glob.glob(os.path.join(cert_dir, 'port_*.pem')):
        filename = os.path.basename(cert_path)
        port_str = filename.replace('port_', '').replace('.pem', '')
        try:
            port_num = int(port_str)
        except ValueError:
            continue

        # Check if expired using openssl
        result = subprocess.run(
            ['openssl', 'x509', '-checkend', '0', '-noout', '-in', cert_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # checkend returns 0 if certificate will not expire before the given time
        # returns 1 if it will expire or has already expired
        if result.returncode != 0:
            expired_ports.append(port_num)

    return sorted(expired_ports)

def test_enforce_sh_exists_and_executable():
    script_path = '/home/user/enforce.sh'
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

def test_enforce_sh_content():
    script_path = '/home/user/enforce.sh'
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    expected_ips = get_expected_ips()
    expected_ports = get_expected_ports()

    expected_lines = ['#!/bin/bash', '# IP Blocklist']
    for ip in expected_ips:
        expected_lines.append(f'iptables -A INPUT -s {ip} -j DROP')

    expected_lines.append('# Port Blocklist')
    for port in expected_ports:
        expected_lines.append(f'iptables -A INPUT -p tcp --dport {port} -j DROP')

    expected_content = '\n'.join(expected_lines) + '\n'

    with open(script_path, 'r') as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"Content of {script_path} does not match expected output.\n"
        f"Expected:\n{expected_content.strip()}\n"
        f"Actual:\n{actual_content.strip()}"
    )