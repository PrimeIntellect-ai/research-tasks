# test_final_state.py

import os
import subprocess
import re

def test_logrotate_config():
    """Verify the logrotate configuration contains the required directives."""
    config_path = "/home/user/logrotate.conf"
    assert os.path.exists(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert re.search(r"\bsize\s+100k\b", content), "logrotate.conf is missing 'size 100k'."
    assert re.search(r"\brotate\s+4\b", content), "logrotate.conf is missing 'rotate 4'."
    assert re.search(r"\bcompress\b", content), "logrotate.conf is missing 'compress'."
    assert re.search(r"\bcopytruncate\b", content), "logrotate.conf is missing 'copytruncate'."

def test_automation_script():
    """Verify the automation script exists, is executable, and contains required commands."""
    script_path = "/home/user/process_metrics.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "/home/user/parser" in content, "process_metrics.sh does not call /home/user/parser."
    assert "logrotate -s /home/user/logrotate.state /home/user/logrotate.conf" in content, \
        "process_metrics.sh does not call logrotate with the correct arguments."

def test_crontab_configuration():
    """Verify the user's crontab has the correct scheduled task."""
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        output = ""

    pattern = r"\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/process_metrics\.sh"
    assert re.search(pattern, output), "Crontab does not contain the correct schedule for process_metrics.sh."

def test_parser_and_execution():
    """Verify the Rust parser is compiled and correctly parses telemetry logs when the script is run."""
    parser_path = "/home/user/parser"
    assert os.path.exists(parser_path), f"{parser_path} binary does not exist."
    assert os.access(parser_path, os.X_OK), f"{parser_path} is not executable."

    log_path = "/home/user/telemetry.log"
    csv_path = "/home/user/memory_dashboard.csv"

    # Write dummy log data
    dummy_logs = (
        "[2023-11-01T10:00:00Z] INFO - disk_space: 45.2\n"
        "[2023-11-01T10:00:01Z] INFO - memory_utilization: 82.1\n"
        "[2023-11-01T10:00:02Z] WARN - cpu_load: 99.9\n"
        "[2023-11-01T10:00:03Z] INFO - memory_utilization: 83.4\n"
    )
    with open(log_path, "w") as f:
        f.write(dummy_logs)

    # Execute the automation script
    subprocess.run(["bash", "/home/user/process_metrics.sh"], check=True)

    assert os.path.exists(csv_path), f"{csv_path} was not created."

    with open(csv_path, "r") as f:
        csv_content = f.read()

    assert "2023-11-01T10:00:01Z,82.1" in csv_content, "CSV is missing the first memory_utilization metric."
    assert "2023-11-01T10:00:03Z,83.4" in csv_content, "CSV is missing the second memory_utilization metric."
    assert "45.2" not in csv_content, "CSV incorrectly contains metrics other than memory_utilization."
    assert "99.9" not in csv_content, "CSV incorrectly contains metrics other than memory_utilization."