# test_final_state.py
import os
import subprocess
import re

def test_script_exists_and_executable():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_etl_pipeline_execution():
    script_path = "/home/user/run_etl.sh"

    # Execute the student's script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

    csv_path = "/home/user/processed/alerts.csv"
    assert os.path.isfile(csv_path), f"Output CSV {csv_path} was not created."

    with open(csv_path, "r") as f:
        csv_content = f.read().strip()

    expected_csv = (
        "epoch,severity,source\n"
        "1697361300,INFO,app\n"
        "1697364270,WARN,sec\n"
        "1697364300,ERROR,app\n"
        "1697364360,CRIT,sec\n"
        "1697364435,FATAL,app"
    )

    assert csv_content == expected_csv, (
        f"CSV content does not match expected output.\n"
        f"Expected:\n{expected_csv}\n\n"
        f"Got:\n{csv_content}"
    )

def test_etl_log_format():
    log_path = "/home/user/etl.log"
    assert os.path.isfile(log_path), f"Pipeline log {log_path} was not created."

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) > 0, f"Pipeline log {log_path} is empty."

    last_line = lines[-1]
    pattern = r"^\[\d{10}\] SUCCESS: processed 5 alerts$"
    assert re.match(pattern, last_line), (
        f"Pipeline log entry does not match expected format or count.\n"
        f"Expected pattern: {pattern}\n"
        f"Got: {last_line}"
    )