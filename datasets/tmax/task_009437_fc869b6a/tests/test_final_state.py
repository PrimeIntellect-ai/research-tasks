# test_final_state.py

import os
import pytest

RESOLUTION_FILE = "/home/user/ticket_resolution.txt"

def test_resolution_file_exists():
    """Verify that the ticket_resolution.txt file exists."""
    assert os.path.exists(RESOLUTION_FILE), f"Missing resolution file: {RESOLUTION_FILE}"
    assert os.path.isfile(RESOLUTION_FILE), f"Not a file: {RESOLUTION_FILE}"

def test_resolution_file_contents():
    """Verify the contents of the ticket_resolution.txt file and the configured directory."""
    assert os.path.exists(RESOLUTION_FILE), f"Missing resolution file: {RESOLUTION_FILE}"

    with open(RESOLUTION_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {RESOLUTION_FILE}, found {len(lines)}"

    # Check Token
    assert lines[0] == "TOKEN: AUTH_SEC_x92bF81mP_99xyz", f"Incorrect TOKEN line: {lines[0]}"

    # Check Crash String
    assert lines[1] == "CRASH_STRING: xzblk", f"Incorrect CRASH_STRING line: {lines[1]}"

    # Check Config Dir
    assert lines[2].startswith("CONFIG_DIR: "), f"Line 3 does not start with 'CONFIG_DIR: ': {lines[2]}"

    config_dir = lines[2].split("CONFIG_DIR: ")[1].strip()
    assert os.path.isabs(config_dir), f"CONFIG_DIR must be an absolute path, got: {config_dir}"

    # Verify settings.ini exists in the specified config dir
    settings_file = os.path.join(config_dir, "settings.ini")
    assert os.path.exists(settings_file), f"Expected settings.ini not found at {settings_file}"
    assert os.path.isfile(settings_file), f"Not a file: {settings_file}"