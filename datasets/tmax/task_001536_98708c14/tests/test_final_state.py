# test_final_state.py

import os
import re
import subprocess
import pytest

def test_crontab_configuration():
    """Verify that the crontab is configured to run the script at the top of every hour."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Has it been set?"

    crontab_content = result.stdout.strip()

    # Check for the expected crontab entry
    # Match minute 0, any hour, any day of month, any month, any day of week
    expected_pattern = r"^0\s+\*\s+\*\s+\*\s+\*\s+/usr/bin/env\s+python3\s+/home/user/process_logs\.py$"

    match_found = any(re.match(expected_pattern, line.strip()) for line in crontab_content.splitlines())
    assert match_found, "Crontab does not contain the correct scheduling for /home/user/process_logs.py"

def test_script_execution_and_output():
    """Run the student's script and verify the output CSV and pipeline log."""
    script_path = "/home/user/process_logs.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Execute the script
    result = subprocess.run(["/usr/bin/env", "python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

    # Check cleaned_logs.csv
    output_csv = "/home/user/cleaned_logs.csv"
    assert os.path.isfile(output_csv), f"Output file {output_csv} was not created."

    with open(output_csv, "r") as f:
        actual_csv = f.read().strip()

    expected_csv = """timestamp,ip_address,method,endpoint,user_agent
2023-10-01T09:55:00Z,192.168.X.X,GET,/api/v1/data,Mozilla/5.0
2023-10-01T10:10:00Z,10.0.X.X,POST,/api/v1/login,curl/7.68.0
2023-10-01T10:15:00Z,172.16.X.X,OPTIONS,/api/v1/data,PostmanRuntime/7.28.4"""

    assert actual_csv == expected_csv, f"Content of {output_csv} does not match expected output."

    # Check pipeline.log
    pipeline_log = "/home/user/pipeline.log"
    assert os.path.isfile(pipeline_log), f"Pipeline log {pipeline_log} was not created."

    with open(pipeline_log, "r") as f:
        log_lines = f.read().strip().splitlines()

    assert len(log_lines) > 0, "Pipeline log is empty."

    last_line = log_lines[-1]

    # Format: [YYYY-MM-DD HH:MM:SS] Processed <N> original rows into <M> deduplicated rows.
    log_pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Processed 5 original rows into 3 deduplicated rows\.$"
    assert re.match(log_pattern, last_line), f"Pipeline log line format or values incorrect. Got: {last_line}"