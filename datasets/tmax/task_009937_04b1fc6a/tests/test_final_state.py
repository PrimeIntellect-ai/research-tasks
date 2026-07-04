# test_final_state.py

import os
import re
import pytest

APP_LOG_PATH = "/home/user/app.log"
CONFIG_INI_PATH = "/home/user/config.ini"
NEW_KEY_PATH = "/home/user/new_key.txt"
OLD_KEY = "DEADc0ffee123456"

def test_app_log_redacted():
    assert os.path.isfile(APP_LOG_PATH), f"File {APP_LOG_PATH} does not exist."

    with open(APP_LOG_PATH, "r") as f:
        content = f.read()

    redacted_count = content.count("[REDACTED]")
    assert redacted_count == 2, f"Expected exactly 2 instances of '[REDACTED]' in {APP_LOG_PATH}, found {redacted_count}."

    assert OLD_KEY not in content, f"Old key {OLD_KEY} is still present in {APP_LOG_PATH}."

    # Check for any remaining weak keys
    weak_keys = re.findall(r'DEAD[0-9a-f]{12}', content)
    assert not weak_keys, f"Found unredacted weak keys in {APP_LOG_PATH}: {weak_keys}"

def test_new_key_generated():
    assert os.path.isfile(NEW_KEY_PATH), f"File {NEW_KEY_PATH} does not exist."

    with open(NEW_KEY_PATH, "r") as f:
        new_key = f.read().strip()

    assert len(new_key) == 32, f"Expected new key to be 32 characters long, got {len(new_key)}."
    assert re.match(r'^[0-9a-f]{32}$', new_key), f"New key '{new_key}' is not a valid 32-character lowercase hex string."

def test_config_ini_updated():
    assert os.path.isfile(CONFIG_INI_PATH), f"File {CONFIG_INI_PATH} does not exist."
    assert os.path.isfile(NEW_KEY_PATH), f"File {NEW_KEY_PATH} does not exist."

    with open(NEW_KEY_PATH, "r") as f:
        new_key = f.read().strip()

    with open(CONFIG_INI_PATH, "r") as f:
        content = f.read()

    assert OLD_KEY not in content, f"Old key {OLD_KEY} is still present in {CONFIG_INI_PATH}."

    expected_line = f"API_KEY={new_key}"
    assert expected_line in content, f"Expected '{expected_line}' not found in {CONFIG_INI_PATH}."