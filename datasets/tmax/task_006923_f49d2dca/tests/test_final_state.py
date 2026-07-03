# test_final_state.py
import os

def test_script_exists_and_executable():
    script_path = "/home/user/check_migration.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_exists():
    report_path = "/home/user/migration_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} was not generated."

def test_report_content():
    report_path = "/home/user/migration_report.txt"
    if not os.path.isfile(report_path):
        return # Handled by previous test

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = """UPGRADES:
pandas 0.24.0
requests 2.20.0
six 1.11.0
urllib3 1.24.2

FAILURES:
legacy.py
old.py
utils.py"""

    assert content == expected_content, (
        f"The content of {report_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{content}"
    )