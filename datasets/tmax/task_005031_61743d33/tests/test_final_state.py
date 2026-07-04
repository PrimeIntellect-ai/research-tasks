# test_final_state.py

import os
import pytest

def test_hardening_report_exists():
    report_path = '/home/user/hardening_report.txt'
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

def test_hardening_report_contents():
    report_path = '/home/user/hardening_report.txt'
    assert os.path.isfile(report_path), "The report file is missing."

    # Compute expected Line 1
    expected_uids = []
    passwd_path = '/home/user/sys_audit/etc_passwd'
    if os.path.isfile(passwd_path):
        with open(passwd_path, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) > 2 and parts[2] == '0' and parts[0] != 'root':
                    expected_uids.append(parts[0])
    expected_line1 = ','.join(expected_uids)

    # Compute expected Line 2
    expected_line2 = ""
    postfix_path = '/home/user/sys_audit/postfix_main.cf'
    if os.path.isfile(postfix_path):
        with open(postfix_path, 'r') as f:
            for line in f:
                if line.startswith('mynetworks') and '=' in line:
                    expected_line2 = line.split('=', 1)[1].strip()
                    break

    # Compute expected Line 3
    expected_line3 = ""
    iptables_path = '/home/user/sys_audit/iptables_save.txt'
    if os.path.isfile(iptables_path):
        with open(iptables_path, 'r') as f:
            for line in f:
                if 'ACCEPT' in line and '--dport' in line:
                    parts = line.split()
                    if '--dport' in parts:
                        idx = parts.index('--dport')
                        try:
                            port = int(parts[idx+1])
                            if port > 1024:
                                expected_line3 = str(port)
                                break
                        except ValueError:
                            pass

    # Compute expected Line 4
    expected_line4_count = 0
    ping_path = '/home/user/sys_audit/ping_results.txt'
    if os.path.isfile(ping_path):
        with open(ping_path, 'r') as f:
            for line in f:
                if '0% packet loss' in line:
                    expected_line4_count += 1
    expected_line4 = str(expected_line4_count)

    # Read the actual report
    with open(report_path, 'r') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    assert len(lines) == 4, f"Expected exactly 4 lines in the report, found {len(lines)}."

    assert lines[0] == expected_line1, f"Line 1 is incorrect. Expected '{expected_line1}', got '{lines[0]}'."
    assert lines[1] == expected_line2, f"Line 2 is incorrect. Expected '{expected_line2}', got '{lines[1]}'."
    assert lines[2] == expected_line3, f"Line 3 is incorrect. Expected '{expected_line3}', got '{lines[2]}'."
    assert lines[3] == expected_line4, f"Line 4 is incorrect. Expected '{expected_line4}', got '{lines[3]}'."