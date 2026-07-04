# test_final_state.py

import os
import re
import subprocess
import pytest
from datetime import datetime

SCRIPT_PATH = '/home/user/init_microservice.py'
CONFIG_DIR = '/home/user/config'
CONFIG_FILE = '/home/user/config/app.env'

def test_config_dir_exists():
    """Verify that the /home/user/config directory exists."""
    assert os.path.isdir(CONFIG_DIR), f"The directory {CONFIG_DIR} does not exist."

def test_script_executable():
    """Verify that the target script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable."

def test_app_env_content_initial():
    """Verify that the configuration file exists and contains the correct initial state."""
    assert os.path.isfile(CONFIG_FILE), f"The config file {CONFIG_FILE} does not exist."

    with open(CONFIG_FILE, 'r') as f:
        content = f.read()

    assert "APP_TZ=Asia/Tokyo" in content, "APP_TZ is not set to Asia/Tokyo in the config file."
    assert "APP_LOCALE=ja_JP.UTF-8" in content, "APP_LOCALE is not set to ja_JP.UTF-8 in the config file."

    match = re.search(r'DEPLOY_TIME=(.*)', content)
    assert match is not None, "DEPLOY_TIME is missing from the config file."

    deploy_time_str = match.group(1).strip()
    try:
        # Check if it's a valid ISO 8601 string
        datetime.fromisoformat(deploy_time_str)
    except ValueError:
        pytest.fail(f"DEPLOY_TIME '{deploy_time_str}' is not a valid ISO 8601 string.")

def test_script_interactive_mode():
    """Verify that the script falls back to interactive mode and prompts correctly."""
    process = subprocess.Popen(
        [SCRIPT_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input="Europe/Paris\nfr_FR.UTF-8\n")

    assert "Enter timezone: " in stdout, "Script did not prompt for timezone correctly."
    assert "Enter locale: " in stdout, "Script did not prompt for locale correctly."

    with open(CONFIG_FILE, 'r') as f:
        content = f.read()

    assert "APP_TZ=Europe/Paris" in content, "Interactive mode did not set APP_TZ correctly."
    assert "APP_LOCALE=fr_FR.UTF-8" in content, "Interactive mode did not set APP_LOCALE correctly."
    assert "DEPLOY_TIME=" in content, "DEPLOY_TIME is missing after interactive mode."

def test_script_cli_args():
    """Verify that the script accepts --tz and --locale arguments."""
    process = subprocess.run(
        [SCRIPT_PATH, '--tz', 'America/New_York', '--locale', 'en_US.UTF-8'],
        capture_output=True,
        text=True
    )
    assert process.returncode == 0, "Script failed when provided with CLI arguments."

    with open(CONFIG_FILE, 'r') as f:
        content = f.read()

    assert "APP_TZ=America/New_York" in content, "CLI arguments did not set APP_TZ correctly."
    assert "APP_LOCALE=en_US.UTF-8" in content, "CLI arguments did not set APP_LOCALE correctly."
    assert "DEPLOY_TIME=" in content, "DEPLOY_TIME is missing after running with CLI arguments."