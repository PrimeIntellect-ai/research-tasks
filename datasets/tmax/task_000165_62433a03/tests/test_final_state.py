# test_final_state.py
import os
import subprocess
import pytest

def get_expected_machine():
    try:
        output = subprocess.check_output(
            ["readelf", "-h", "/home/user/audit_target/app_bin"], 
            text=True
        )
        for line in output.splitlines():
            if "Machine:" in line:
                # Extract the part after 'Machine:' and strip leading/trailing whitespace
                return line.split("Machine:")[1].strip()
    except Exception as e:
        return None
    return None

def test_audit_report_exists_and_correct():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"The audit report file {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_machine = get_expected_machine()
    assert expected_machine is not None, "Could not determine expected machine type from app_bin."

    expected_lines = [
        "[AUDIT TRAIL]",
        f"Binary_Machine: {expected_machine}",
        "Cert_Status: VALID",
        "CSP_Status: ENFORCED"
    ]
    expected_content = "\n".join(expected_lines)

    # Normalize line endings
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(content_lines) == 4, f"Expected 4 lines in the report, but got {len(content_lines)}."
    assert content_lines[0] == expected_lines[0], f"Expected first line to be '{expected_lines[0]}', got '{content_lines[0]}'."
    assert content_lines[1] == expected_lines[1], f"Expected Binary_Machine line to be '{expected_lines[1]}', got '{content_lines[1]}'."
    assert content_lines[2] == expected_lines[2], f"Expected Cert_Status line to be '{expected_lines[2]}', got '{content_lines[2]}'."
    assert content_lines[3] == expected_lines[3], f"Expected CSP_Status line to be '{expected_lines[3]}', got '{content_lines[3]}'."