# test_final_state.py

import os
import re
import stat
import pytest

SCRIPT_PATH = "/home/user/process_timeseries.sh"
OUTPUT_FILE = "/home/user/data/processed/metrics_summary.csv"
LOG_FILE = "/home/user/logs/pipeline.log"
CRON_FILE = "/home/user/crontab.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_output_file_content():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

    with open(OUTPUT_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "2023-10-01,cpu_usage,45.2",
        "2023-10-01,disk_io,10.5",
        "2023-10-02,cpu_usage,55.0",
        "2023-10-02,memory_usage,2048"
    ]

    assert sorted(lines) == sorted(expected_lines), "The content of metrics_summary.csv does not match the expected output."

def test_log_file_content():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."

    with open(LOG_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines, "Log file is empty."

    last_line = lines[-1]

    # Expected format: [YYYY-MM-DD HH:MM:SS] Pipeline completed. Processed 4 valid records.
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Pipeline completed\. Processed 4 valid records\.$"
    assert re.match(pattern, last_line), f"Log entry format is incorrect. Found: {last_line}"

def test_crontab_file():
    assert os.path.isfile(CRON_FILE), f"Crontab file {CRON_FILE} does not exist."

    with open(CRON_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    expected_cron = "0 2 * * * /home/user/process_timeseries.sh"

    found = any(expected_cron in line or re.sub(r'\s+', ' ', line) == expected_cron for line in lines)
    assert found, f"Expected cron expression not found in {CRON_FILE}. Ensure it runs at 2:00 AM daily."