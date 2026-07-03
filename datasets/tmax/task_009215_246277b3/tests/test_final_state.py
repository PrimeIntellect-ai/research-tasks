# test_final_state.py

import os

def test_verify_migration_script_exists():
    script_path = "/home/user/verify_migration.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_test_report_exists_and_correct():
    report_path = "/home/user/test_report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    expected_lines = ["art-2", "art-4"]

    assert lines == expected_lines, (
        f"The contents of {report_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Got:\n{chr(10).join(lines)}"
    )