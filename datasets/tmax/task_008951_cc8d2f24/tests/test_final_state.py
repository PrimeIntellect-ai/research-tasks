# test_final_state.py

import os
import re
import subprocess
import stat
import pytest

def test_bashrc_timezone():
    """Check that APP_TIMEZONE="Asia/Tokyo" is in /home/user/.bashrc."""
    bashrc_path = '/home/user/.bashrc'
    assert os.path.isfile(bashrc_path), f"{bashrc_path} is missing."
    with open(bashrc_path, 'r') as f:
        content = f.read()
    assert 'APP_TIMEZONE="Asia/Tokyo"' in content or "APP_TIMEZONE='Asia/Tokyo'" in content or "APP_TIMEZONE=Asia/Tokyo" in content, \
        "APP_TIMEZONE setup is missing or incorrect in .bashrc."

def test_go_files_exist():
    """Check that the required Go files exist."""
    go_files = [
        '/home/user/backend.go',
        '/home/user/lb.go',
        '/home/user/forwarder.go'
    ]
    for gf in go_files:
        assert os.path.isfile(gf), f"Go source file {gf} is missing."

def test_run_system_script_executable():
    """Check that run_system.sh exists and is executable."""
    script_path = '/home/user/run_system.sh'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_execution_and_log_verification():
    """Run the script if needed, and verify the log file contents."""
    log_path = '/home/user/test_results.log'
    script_path = '/home/user/run_system.sh'

    if not os.path.isfile(log_path):
        # Run the script to generate the log
        result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        assert os.path.isfile(log_path), f"Log file {log_path} was not created after running the script."

    with open(log_path, 'r') as f:
        log_content = f.read()

    # Check for backend responses
    count_8081 = len(re.findall(r'Backend responding from port 8081', log_content))
    count_8082 = len(re.findall(r'Backend responding from port 8082', log_content))

    assert count_8081 == 2, f"Expected exactly 2 responses from port 8081, found {count_8081}."
    assert count_8082 == 2, f"Expected exactly 2 responses from port 8082, found {count_8082}."

    # Check for X-Forwarded-Time header with +09:00 timezone
    time_headers = re.findall(r'X-Forwarded-Time:.*?\+09:00', log_content, re.IGNORECASE)
    assert len(time_headers) == 4, f"Expected exactly 4 'X-Forwarded-Time' headers with '+09:00' timezone, found {len(time_headers)}."