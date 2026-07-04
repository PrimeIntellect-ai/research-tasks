# test_final_state.py
import os
import subprocess

def test_audit_report_content():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    expected_output = (
        "U_03,DB_A,EXT_Z,1002,1008\n"
        "U_04,DB_C,EXT_X,1003,1010\n"
        "U_05,DB_A,EXT_W,1004,1005\n"
    )

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_output.strip(), f"Content of {report_path} does not match expected output."

def test_c_program_exists_and_compiles():
    c_file = "/home/user/graph_audit.c"
    executable = "/home/user/graph_audit"

    assert os.path.isfile(c_file), f"C source file {c_file} is missing."
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_executable_logic():
    executable = "/home/user/graph_audit"
    csv_file = "/home/user/system_logs.csv"

    # Test with limit 2, offset 0
    cmd = [executable, csv_file, "2", "0"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    expected = (
        "U_01,DB_A,EXT_Z,1000,1005\n"
        "U_02,DB_B,EXT_Y,1001,1006\n"
    )

    assert result.returncode == 0, "Executable returned non-zero exit code."
    assert result.stdout.strip() == expected.strip(), "Executable output did not match expected logic for limit 2 offset 0."