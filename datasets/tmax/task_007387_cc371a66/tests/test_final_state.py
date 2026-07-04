# test_final_state.py
import os
import re
import subprocess
import pytest

def test_rust_binary_behavior():
    binary_path = "/home/user/finops-analyzer/target/release/finops-analyzer"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}. Did you build in release mode?"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable."

    test_csv = (
        "ResourceID,Type,Status,Cost\n"
        "i-123,ec2,running,10.50\n"
        "i-124,ec2,idle,5.25\n"
        "i-125,ec2,IDLE,15.00\n"
        "db-1,rds,stopped,0.00\n"
        "db-2,rds,idle,100.50\n"
    )

    result = subprocess.run(
        [binary_path],
        input=test_csv.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output = result.stdout.decode("utf-8").strip()
    assert output == "120.75", f"Expected output '120.75', but got '{output}'"

def test_script_execution():
    script_path = "/home/user/run_analysis.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable."

    log_path = "/home/user/logs/idle_costs.log"

    # Run the script
    subprocess.run([script_path], check=True)

    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) > 0, "Log file is empty."
    last_line = lines[-1].strip()

    # regex: ^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}\] Total idle cost: \$120\.75$
    # Also allowing Z for UTC in ISO-8601
    pattern = r"^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)\] Total idle cost: \$120\.75$"
    assert re.match(pattern, last_line), f"Log line format incorrect. Got: '{last_line}'"

def test_logrotate_config():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config not found at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/logs/idle_costs.log" in content, "Target log file missing in logrotate.conf"
    assert "daily" in content, "'daily' missing in logrotate.conf"
    assert "rotate 7" in content, "'rotate 7' missing in logrotate.conf"
    assert "compress" in content, "'compress' missing in logrotate.conf"
    assert "missingok" in content, "'missingok' missing in logrotate.conf"

def test_crontab():
    result = subprocess.run(
        ["crontab", "-l"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # It might be empty or fail if no crontab exists, but we expect it to exist
    assert result.returncode == 0, "Failed to read crontab. Has it been created?"

    crontab_content = result.stdout.decode("utf-8")

    # Look for the exact schedule and script
    # e.g., 0 * * * * /home/user/run_analysis.sh
    # allow some spaces
    pattern = r"^0\s+\*\s+\*\s+\*\s+\*\s+/home/user/run_analysis\.sh"

    match_found = any(re.match(pattern, line.strip()) for line in crontab_content.splitlines())
    assert match_found, f"Crontab does not contain the correct schedule for run_analysis.sh. Crontab content:\n{crontab_content}"