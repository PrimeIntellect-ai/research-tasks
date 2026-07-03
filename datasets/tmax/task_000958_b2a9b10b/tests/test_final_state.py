# test_final_state.py
import os
import subprocess
import pytest

def test_elf_audit_c_exists():
    """Verify that the C source file exists and includes <elf.h>."""
    path = "/home/user/elf_audit.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "<elf.h>" in content, f"{path} does not include <elf.h>."

def test_elf_audit_executable_exists():
    """Verify that the compiled elf_audit binary exists and is executable."""
    path = "/home/user/elf_audit"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_audit_report():
    """Verify the contents of the audit report."""
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Report {report_path} does not exist."

    # Compute expected entry point using readelf
    server_bin = "/home/user/server_bin"
    try:
        out = subprocess.check_output(["readelf", "-h", server_bin], universal_newlines=True)
        entry_point = None
        for line in out.splitlines():
            if "Entry point address:" in line:
                entry_point = line.split(":", 1)[1].strip()
                break
        assert entry_point is not None, "Could not determine entry point from server_bin."
    except Exception as e:
        pytest.fail(f"Failed to run readelf: {e}")

    # Compute expected expiry using openssl
    server_crt = "/home/user/server.crt"
    try:
        out = subprocess.check_output(["openssl", "x509", "-in", server_crt, "-noout", "-enddate"], universal_newlines=True)
        expiry = out.strip().split("=", 1)[1]
    except Exception as e:
        pytest.fail(f"Failed to run openssl: {e}")

    # Read and verify report
    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Audit report should have exactly 2 lines, found {len(lines)}."

    expected_line1 = f"Entry: {entry_point}"
    expected_line2 = f"Expiry: {expiry}"

    assert lines[0] == expected_line1, f"Line 1 mismatch. Expected '{expected_line1}', got '{lines[0]}'."
    assert lines[1] == expected_line2, f"Line 2 mismatch. Expected '{expected_line2}', got '{lines[1]}'."