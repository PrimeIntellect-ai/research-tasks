# test_final_state.py

import os
import stat
import pytest

def test_c_source_exists():
    c_file = "/home/user/src/quota_calc.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

def test_c_executable_exists_and_is_elf():
    exe_file = "/home/user/bin/quota_calc"
    assert os.path.isfile(exe_file), f"Executable {exe_file} is missing."

    # Check if it has execute permissions
    st = os.stat(exe_file)
    assert st.st_mode & stat.S_IXUSR, f"File {exe_file} is not executable."

    # Check if it's an ELF file
    with open(exe_file, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"File {exe_file} is not a valid ELF executable."

def test_bash_script_exists_and_executable():
    script_file = "/home/user/bin/run_checks.sh"
    assert os.path.isfile(script_file), f"Bash script {script_file} is missing."

    # Check if it has execute permissions
    st = os.stat(script_file)
    assert st.st_mode & stat.S_IXUSR, f"Bash script {script_file} is not executable."

def test_report_exists_and_contents():
    report_file = "/home/user/logs/quota_report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} is missing."

    expected_lines = [
        "/home/user/users/alice TOTAL_BYTES: 6000 STATUS: OK",
        "/home/user/users/bob TOTAL_BYTES: 15000 STATUS: EXCEEDED",
        "/home/user/users/charlie TOTAL_BYTES: 12000 STATUS: EXCEEDED"
    ]

    with open(report_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Report file contents do not match expected.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )