# test_final_state.py

import os
import re

def test_hourly_failures_csv_content():
    csv_path = "/home/user/hourly_failures.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "2023-10-24 14:00:00,192.168.1.50,admin_2,2",
        "2023-10-24 15:00:00,999.999.999.999,valid_user,1",
        "2023-10-24 16:00:00,10.0.0.2,bob,2",
        "2023-10-24 16:00:00,192.168.0.1,alice,1"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch in {csv_path}.\nExpected: {expected}\nActual:   {actual}"

def test_run_parser_sh_executable():
    script_path = "/home/user/run_parser.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable (+x)."

def test_log_cron_configuration():
    cron_path = "/home/user/log_cron"
    assert os.path.exists(cron_path), f"Cron configuration file {cron_path} is missing."

    with open(cron_path, "r") as f:
        content = f.read()

    # Look for a line that starts with "0 * * * *" (allowing for variable whitespace)
    # and ideally contains the script path.
    valid_cron_pattern = re.compile(r"^0\s+\*\s+\*\s+\*\s+\*.*", re.MULTILINE)

    assert valid_cron_pattern.search(content), (
        f"File {cron_path} does not contain the correct cron expression ('0 * * * *').\n"
        f"Found content:\n{content}"
    )