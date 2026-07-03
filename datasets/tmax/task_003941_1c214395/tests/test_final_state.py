# test_final_state.py

import os
import re

LOG_FILE = "/home/user/network_logs/status.log"
SCRIPT_FILE = "/home/user/scripts/monitor.py"

def test_log_file_exists():
    """Test that the status.log file was created in the correct directory."""
    assert os.path.isfile(LOG_FILE), f"The log file {LOG_FILE} does not exist. Did you run the script?"

def test_log_file_content():
    """Test that the log file contains the correctly formatted string."""
    assert os.path.isfile(LOG_FILE), f"The log file {LOG_FILE} does not exist."

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"The log file {LOG_FILE} is empty."

    # Regex to match: [YYYY-MM-DD HH:MM:SS] [America/New_York] STATUS: OK - Latency 14ms
    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] \[America/New_York\] STATUS: OK - Latency 14ms$")

    match_found = any(pattern.match(line.strip()) for line in lines)
    assert match_found, f"No line in {LOG_FILE} matched the expected format and timezone."

def test_script_fixes():
    """Test that the monitor.py script contains the required fixes."""
    assert os.path.isfile(SCRIPT_FILE), f"The script {SCRIPT_FILE} is missing."

    with open(SCRIPT_FILE, "r") as f:
        content = f.read()

    # Check for absolute path to netcheck
    assert "/home/user/bin/netcheck" in content, "The script does not use the absolute path to netcheck."

    # Check for absolute path to log file
    assert "/home/user/network_logs/status.log" in content, "The script does not use the absolute path for the log file."

    # Check for timezone logic
    assert "America/New_York" in content, "The script does not reference 'America/New_York'."
    has_zoneinfo = "zoneinfo" in content or "ZoneInfo" in content
    has_pytz = "pytz" in content
    assert has_zoneinfo or has_pytz, "The script must use 'zoneinfo' or 'pytz' for timezone handling."