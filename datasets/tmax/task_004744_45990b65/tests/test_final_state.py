# test_final_state.py

import os
import re

def test_cron_file_exists_and_correct():
    cron_path = "/home/user/pipeline.cron"
    assert os.path.isfile(cron_path), f"Cron file {cron_path} does not exist."

    with open(cron_path, "r") as f:
        content = f.read()

    # Check if the required cron string is in the file
    expected_cron = r"15\s+\*\s+\*\s+\*\s+\*\s+/home/user/bin/process_events"
    assert re.search(expected_cron, content), f"Cron configuration is incorrect. Expected to find '15 * * * * /home/user/bin/process_events' in {cron_path}."

def test_executable_exists():
    exe_path = "/home/user/bin/process_events"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_processed_events_output():
    output_path = "/home/user/data/processed_events.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_lines = [
        "2023-10-25-14,a***@corp.com,300",
        "2023-10-25-14,b***@startup.io,50",
        "2023-10-25-15,b***@startup.io,150",
        "2023-10-25-15,c***@domain.com,300",
        "2023-10-25-15,d***@test.com,50",
        "2023-10-26-09,a***@corp.com,500"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The contents of processed_events.csv do not match the expected aggregated output. Ensure bad rows are dropped, emails are anonymized correctly, amounts are summed, and output is sorted."