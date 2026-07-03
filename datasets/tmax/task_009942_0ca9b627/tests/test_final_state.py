# test_final_state.py

import os
import re

def test_forensics_report():
    report_path = "/home/user/forensics_report.txt"

    assert os.path.exists(report_path), f"Report file missing: {report_path}"
    assert os.path.isfile(report_path), f"Path is not a file: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in the report, found {len(lines)}"

    port_match = re.match(r"^Port:\s*(\d+)$", lines[0])
    assert port_match, f"Line 1 does not match 'Port: [port number]'. Found: {lines[0]}"
    assert port_match.group(1) == "44444", f"Expected Port 44444, found {port_match.group(1)}"

    payload_match = re.match(r"^Payload:\s*(.+)$", lines[1])
    assert payload_match, f"Line 2 does not match 'Payload: [payload]'. Found: {lines[1]}"
    assert payload_match.group(1) == "<img src=x onerror=alert('pwned')>", f"Expected Payload '<img src=x onerror=alert('pwned')>', found {payload_match.group(1)}"

    hash_match = re.match(r"^Hash:\s*([a-fA-F0-9]{64})$", lines[2])
    assert hash_match, f"Line 3 does not match 'Hash: [SHA-256 hash]'. Found: {lines[2]}"
    assert hash_match.group(1).lower() == "f17711fde97843d1a473c22ff7ee8c15eb18daec3ce9516d2f3c30ea515cc606", f"Expected Hash f17711fde97843d1a473c22ff7ee8c15eb18daec3ce9516d2f3c30ea515cc606, found {hash_match.group(1)}"