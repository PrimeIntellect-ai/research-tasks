# test_final_state.py
import os

def test_triage_report_exists():
    path = "/home/user/triage_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create the report?"

def test_triage_report_content():
    path = "/home/user/triage_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_failing_line = "INFO: CRITICAL_RACE_CONDITION_883 in module auth_service"
    expected_syscall = "futex"

    failing_line_found = False
    syscall_found = False

    for line in lines:
        if line.startswith("FAILING_LINE:"):
            val = line.split("FAILING_LINE:", 1)[1].strip()
            assert val == expected_failing_line, f"Incorrect FAILING_LINE. Expected '{expected_failing_line}', got '{val}'"
            failing_line_found = True
        elif line.startswith("SYSCALL:"):
            val = line.split("SYSCALL:", 1)[1].strip()
            assert val == expected_syscall, f"Incorrect SYSCALL. Expected '{expected_syscall}', got '{val}'"
            syscall_found = True

    assert failing_line_found, "The report is missing the 'FAILING_LINE:' entry."
    assert syscall_found, "The report is missing the 'SYSCALL:' entry."