# test_final_state.py
import os
import json
import hashlib
import configparser
import subprocess
import pytest

EXPLOIT_GENERATOR_PATH = "/home/user/exploit_generator.py"
EXPLOIT_JSON_PATH = "/home/user/exploit.json"
TARGET_WAF_PATH = "/home/user/target/waf_eval.py"
CONFIG_PATH = "/home/user/target/config.ini"
PWNED_FILE_PATH = "/home/user/pwned.txt"

def test_exploit_generator_exists():
    """Verify the student created the exploit generator script."""
    assert os.path.isfile(EXPLOIT_GENERATOR_PATH), f"File missing: {EXPLOIT_GENERATOR_PATH}"

def test_exploit_generation():
    """Run the generator script and verify it creates the exploit.json file."""
    # Ensure a clean state
    if os.path.exists(EXPLOIT_JSON_PATH):
        os.remove(EXPLOIT_JSON_PATH)

    result = subprocess.run(
        ["python3", EXPLOIT_GENERATOR_PATH],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Generator script failed with error:\n{result.stderr}"
    assert os.path.isfile(EXPLOIT_JSON_PATH), f"Generator script did not create {EXPLOIT_JSON_PATH}"

def test_exploit_json_structure_and_token():
    """Verify the structure of exploit.json and the correctness of the forged token."""
    assert os.path.isfile(EXPLOIT_JSON_PATH), f"Cannot test structure, {EXPLOIT_JSON_PATH} is missing."

    with open(EXPLOIT_JSON_PATH, 'r') as f:
        try:
            req = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"exploit.json is not valid JSON: {e}")

    # Check structure
    assert "headers" in req, "exploit.json missing 'headers' key."
    assert "body" in req, "exploit.json missing 'body' key."

    headers = req["headers"]
    body = req["body"]

    assert "Cookie" in headers, "Missing 'Cookie' in headers."
    assert "X-Bypass-Token" in headers, "Missing 'X-Bypass-Token' in headers."
    assert "payload" in body, "Missing 'payload' in body."
    assert isinstance(body["payload"], str) and body["payload"], "Payload must be a non-empty string."

    # Validate the token logically
    assert os.path.isfile(CONFIG_PATH), f"Missing config file {CONFIG_PATH} to check token."
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    salt = config['security']['secret_salt']

    cookie = headers["Cookie"]
    expected_token = hashlib.md5((cookie + salt).encode()).hexdigest()
    actual_token = headers["X-Bypass-Token"]

    assert actual_token == expected_token, f"Forged token '{actual_token}' does not match expected token '{expected_token}'."

def test_sandbox_escape_execution():
    """Run the WAF target with the generated exploit and verify the sandbox escape succeeds."""
    assert os.path.isfile(EXPLOIT_JSON_PATH), f"Cannot run exploit, {EXPLOIT_JSON_PATH} is missing."

    # Ensure a clean state for the pwned file
    if os.path.exists(PWNED_FILE_PATH):
        os.remove(PWNED_FILE_PATH)

    result = subprocess.run(
        ["python3", TARGET_WAF_PATH, EXPLOIT_JSON_PATH],
        capture_output=True,
        text=True
    )

    # Check if the sandbox was escaped and the file was written
    assert os.path.isfile(PWNED_FILE_PATH), (
        f"Sandbox escape failed. {PWNED_FILE_PATH} was not created.\n"
        f"WAF stdout: {result.stdout}\n"
        f"WAF stderr: {result.stderr}"
    )

    # Verify the content of the pwned file
    with open(PWNED_FILE_PATH, 'r') as f:
        content = f.read()

    assert "Pwned!" in content, f"Incorrect content in {PWNED_FILE_PATH}. Expected 'Pwned!', got '{content}'."