# test_final_state.py

import os

INCIDENT_DIR = "/home/user/incident"
ENV_FILE = os.path.join(INCIDENT_DIR, ".env")
SUCCESS_LOG = os.path.join(INCIDENT_DIR, "success.log")
VALIDATE_SCRIPT = os.path.join(INCIDENT_DIR, "validate.sh")
EXPECTED_TOKEN = "sec_k93jD82hf8z"

def test_env_file_exists_and_correct():
    assert os.path.isfile(ENV_FILE), f"The file {ENV_FILE} does not exist. Did you create it?"
    with open(ENV_FILE, "r") as f:
        content = f.read().strip()

    expected_line = f"API_TOKEN={EXPECTED_TOKEN}"
    assert expected_line in content, f"{ENV_FILE} does not contain the correct API_TOKEN line. Expected '{expected_line}'."

def test_validate_script_is_fixed():
    assert os.path.isfile(VALIDATE_SCRIPT), f"The script {VALIDATE_SCRIPT} is missing."
    with open(VALIDATE_SCRIPT, "r") as f:
        content = f.read()

    assert "val2=5" in content, "The script validate.sh was not correctly fixed. Expected 'val2=5'."
    assert "val2=0" not in content, "The script validate.sh still contains the bug 'val2=0'."

def test_success_log_exists_and_correct():
    assert os.path.isfile(SUCCESS_LOG), f"The file {SUCCESS_LOG} does not exist. Did you run the script successfully?"
    with open(SUCCESS_LOG, "r") as f:
        content = f.read().strip()

    expected_msg = f"Pipeline executed successfully with token {EXPECTED_TOKEN}"
    assert content == expected_msg, f"The contents of {SUCCESS_LOG} are incorrect. Expected '{expected_msg}', but got '{content}'."