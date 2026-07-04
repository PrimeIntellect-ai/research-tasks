# test_final_state.py

import os
import re
import pytest

MONITOR_DIR = "/home/user/monitor"
DATA_DIR = os.path.join(MONITOR_DIR, "data")
SCRIPT_PATH = os.path.join(MONITOR_DIR, "uptime_monitor.sh")
CONFIG_PATH = os.path.join(MONITOR_DIR, "config.env")
LOG_PATH = os.path.join(DATA_DIR, "uptime.log")
REPORT_PATH = os.path.join(MONITOR_DIR, "report.txt")

def test_uptime_log_cleaned():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} is missing."
    with open(LOG_PATH, "r") as f:
        lines = f.read().strip().splitlines()

    valid_format = re.compile(r"^\d{4}-\d{2}-\d{2}\|\d+(\.\d+)?$")

    for line in lines:
        if not line.strip():
            continue
        assert valid_format.match(line), f"Found malformed line in log: {line}"

    # Check that valid historical data is still there
    expected_dates = ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-06", "2023-10-07"]
    found_dates = [line.split("|")[0] for line in lines if line.strip()]

    for date in expected_dates:
        assert date in found_dates, f"Valid historical data for {date} is missing from the log."

def test_config_env_secret_restored():
    assert os.path.isfile(CONFIG_PATH), f"Config file {CONFIG_PATH} is missing."
    with open(CONFIG_PATH, "r") as f:
        content = f.read()

    # The secret from git history is SRE_secret_8841a
    assert 'API_KEY="SRE_secret_8841a"' in content or "API_KEY='SRE_secret_8841a'" in content or "API_KEY=SRE_secret_8841a" in content, \
        "The correct API_KEY was not restored to config.env."

def test_uptime_script_bug_fixed():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    # Check for some form of retries increment
    increment_patterns = [
        r"retries=\$\(\(retries\s*\+\s*1\)\)",
        r"let\s+retries\+\+",
        r"retries=\$\(expr\s+\$retries\s*\+\s*1\)",
        r"\(\(\s*retries\+\+\s*\)\)",
        r"retries=\$\[\s*retries\s*\+\s*1\s*\]"
    ]

    fixed = any(re.search(pattern, content) for pattern in increment_patterns)
    assert fixed, "The infinite loop bug in uptime_monitor.sh does not appear to be fixed (missing 'retries' increment)."

def test_report_generated_and_correct():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing. Did you run the script?"

    with open(REPORT_PATH, "r") as f:
        content = f.read()

    assert "API_STATUS=OK" in content, "The report does not contain API_STATUS=OK. The secret may be wrong or the script failed."

    # Calculate expected average from the cleaned log
    with open(LOG_PATH, "r") as f:
        lines = [line for line in f.read().strip().splitlines() if line.strip()]

    total = 0.0
    count = 0
    for line in lines:
        parts = line.split("|")
        if len(parts) == 2:
            try:
                total += float(parts[1])
                count += 1
            except ValueError:
                pass

    expected_avg = round(total / count, 2) if count > 0 else 0.0

    # The bash script uses `bc` with scale=2 which truncates instead of rounding, 
    # but for these specific values (99.9+100.0+99.5+98.2+99.1+100.0 = 596.7 / 6 = 99.45) it is exact.
    expected_avg_str = f"{expected_avg:.2f}"

    assert f"Average Uptime={expected_avg_str}" in content, \
        f"The report does not contain the correct Average Uptime. Expected Average Uptime={expected_avg_str}"