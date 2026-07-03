# test_final_state.py

import os
import stat
import re

def test_process_reports_c_exists():
    """Verify /home/user/process_reports.c exists."""
    assert os.path.isfile("/home/user/process_reports.c"), "/home/user/process_reports.c does not exist."

def test_run_pipeline_sh_exists_and_executable():
    """Verify /home/user/run_pipeline.sh exists and is executable."""
    filepath = "/home/user/run_pipeline.sh"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    st = os.stat(filepath)
    assert bool(st.st_mode & stat.S_IXUSR), f"{filepath} is not executable by the user."

def test_processed_csv_files_exist():
    """Verify processed CSV files exist."""
    expected_files = ["day1.csv", "day2.csv", "day3.csv"]
    for filename in expected_files:
        filepath = f"/home/user/processed/{filename}"
        assert os.path.isfile(filepath), f"{filepath} does not exist."

def test_processed_csv_file_contents():
    """Verify the contents of /home/user/processed/day1.csv."""
    filepath = "/home/user/processed/day1.csv"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Date,State,Token",
        "2023-11-01,NY,hello",
        "2023-11-01,NY,world",
        "2023-11-01,CA,nothing",
        "2023-11-01,CA,to",
        "2023-11-01,CA,report",
        "2023-11-01,TX,critical",
        "2023-11-01,TX,error",
        "2023-11-01,TX,on",
        "2023-11-01,TX,db",
        "2023-11-02,NY,all",
        "2023-11-02,NY,systems",
        "2023-11-02,NY,go",
        "2023-11-02,CA,running",
        "2023-11-02,CA,smoothly",
        "2023-11-02,TX,wait",
        "2023-11-02,TX,what"
    ]

    # We will check if the expected lines are present in the correct order
    # Some implementations might quote fields or have slightly different spacing
    # but the simplest valid CSV is an exact match.
    assert lines == expected_lines, f"Contents of {filepath} do not match expected output."

def test_cron_backup_exists_and_contains_job():
    """Verify /home/user/cron_backup.txt contains the expected cron job."""
    filepath = "/home/user/cron_backup.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read()

    # Look for a line matching '30 2 * * *' and the script path
    match = re.search(r'^30\s+2\s+\*\s+\*\s+\*.*/home/user/run_pipeline\.sh', content, re.MULTILINE)
    assert match is not None, f"Cron job '30 2 * * * /home/user/run_pipeline.sh' not found in {filepath}."