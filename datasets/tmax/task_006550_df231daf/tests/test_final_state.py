# test_final_state.py
import os
import csv
import stat

def test_audit_trail_csv():
    csv_path = '/home/user/audit_trail.csv'
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    expected_header = ['Timestamp', 'Attacker_IP', 'Vulnerable_Endpoint', 'Missing_Security_Headers']
    expected_rows = [
        ['2023-10-25T10:00:00Z', '192.168.1.50', '/api/v1/search', 'True'],
        ['2023-10-25T10:30:00Z', '192.168.1.100', '/api/v1/search', 'True'],
        ['2023-10-25T11:00:00Z', '203.0.113.5', '/api/v1/search', 'False']
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{csv_path} is empty."
    assert rows[0] == expected_header, f"Header row in {csv_path} is incorrect. Expected {expected_header}, got {rows[0]}"

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, found {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_block_ips_script():
    script_path = '/home/user/block_ips.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Check executable permission
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    expected_lines = [
        "iptables -A INPUT -s 192.168.1.100 -j DROP",
        "iptables -A INPUT -s 192.168.1.50 -j DROP",
        "iptables -A INPUT -s 203.0.113.5 -j DROP"
    ]

    with open(script_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} iptables rules, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Rule {i+1} mismatch in {script_path}. Expected '{expected}', got '{actual}'."