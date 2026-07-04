# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_block_routes_script_exists_and_executable():
    script_path = "/home/user/block_routes.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

def test_block_routes_content():
    script_path = "/home/user/block_routes.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    expected_lines = [
        "ip route add blackhole 192.168.1.50",
        "ip route add blackhole 172.16.0.10"
    ]

    for line in expected_lines:
        assert line in content, f"Expected command '{line}' not found in {script_path}."

    unexpected_line = "ip route add blackhole 10.0.0.5"
    assert unexpected_line not in content, f"Unexpected command '{unexpected_line}' found in {script_path}."

def test_cron_job_configured():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("crontab -l failed, cron job might not be configured.")

    # Regex to match every 5 minutes: '*/5 * * * *' followed by python path and script path
    pattern = r"^\s*(?:\*/5|0-59/5)\s+\*\s+\*\s+\*\s+\*\s+/usr/bin/python3\s+/home/user/analyze_auth\.py\s*$"

    match_found = False
    for line in output.splitlines():
        if re.match(pattern, line):
            match_found = True
            break

    assert match_found, "Cron job for analyze_auth.py every 5 minutes was not found in crontab."

def test_python_script_missing_log_handling(tmp_path):
    script_path = "/home/user/analyze_auth.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."

    log_path = "/home/user/auth.log"
    backup_path = "/home/user/auth.log.bak"

    # Temporarily move the log file if it exists
    log_moved = False
    if os.path.exists(log_path):
        os.rename(log_path, backup_path)
        log_moved = True

    try:
        # Run the script
        result = subprocess.run(
            ["/usr/bin/python3", script_path],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Script exited with non-zero code {result.returncode} when log is missing."
        assert "Log not found" in result.stdout, "Script did not print 'Log not found' when log is missing."
    finally:
        # Restore the log file
        if log_moved:
            os.rename(backup_path, log_path)