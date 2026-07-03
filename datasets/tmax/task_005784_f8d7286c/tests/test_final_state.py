# test_final_state.py

import os

def test_recovery_report_exists():
    """Test that the recovery_report.txt file was created."""
    report_path = "/home/user/recovery_report.txt"
    assert os.path.exists(report_path), f"{report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

def test_recovery_report_contents():
    """Test that the contents of recovery_report.txt match the expected output."""
    report_path = "/home/user/recovery_report.txt"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "db.ini:192.168.1.100",
        "web.ini:4"
    ]

    # The task specifies the lines must be sorted alphabetically
    expected_sorted = sorted(expected)

    assert lines == expected_sorted, f"Report content mismatch. Expected {expected_sorted}, got {lines}"

def test_safe_configs_directory_exists():
    """Test that the safe_configs directory exists."""
    safe_configs_path = "/home/user/safe_configs"
    assert os.path.isdir(safe_configs_path), f"{safe_configs_path} directory is missing."

def test_renamed_ini_files_exist():
    """Test that the renamed .ini files exist in safe_configs."""
    safe_configs_path = "/home/user/safe_configs"
    db_ini_path = os.path.join(safe_configs_path, "db.ini")
    web_ini_path = os.path.join(safe_configs_path, "web.ini")

    assert os.path.isfile(db_ini_path), f"{db_ini_path} is missing."
    assert os.path.isfile(web_ini_path), f"{web_ini_path} is missing."