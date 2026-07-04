# test_final_state.py

import os
import subprocess
import csv
import stat

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} does not have execute permissions for the user."

def test_data_web_log_exists():
    log_path = "/home/user/data/web.log"
    assert os.path.exists(log_path), f"The copied log file {log_path} does not exist. Did the pipeline run?"
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    # Verify it has some content
    assert os.path.getsize(log_path) > 0, f"{log_path} is empty."

def test_anomalies_csv_content():
    csv_path = "/home/user/anomalies.csv"
    assert os.path.exists(csv_path), f"The anomalies file {csv_path} does not exist."

    expected_rows = [
        ["Timestamp", "IP", "ResponseTime"],
        ["2023-10-01T12:00:06", "192.168.1.100", "150"],
        ["2023-10-01T12:00:09", "192.168.1.101", "200"]
    ]

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"The content of {csv_path} does not match the expected anomalies."

def test_crontab_configured():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run 'crontab -l' or no crontab exists for the user.")

    lines = [line.strip() for line in output.split("\n") if line.strip() and not line.strip().startswith("#")]

    # Look for a cron job that runs every 5 minutes and executes run_pipeline.sh
    found = False
    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            minute = parts[0]
            command = " ".join(parts[5:])
            if (minute == "*/5" or minute == "0,5,10,15,20,25,30,35,40,45,50,55") and "/home/user/run_pipeline.sh" in command:
                found = True
                break

    assert found, "Could not find a crontab entry running /home/user/run_pipeline.sh every 5 minutes."