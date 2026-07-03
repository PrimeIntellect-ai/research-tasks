# test_final_state.py

import os
import subprocess
import random
import string
import pytest

AGENT_SCRIPT = "/home/user/generate_manifest.sh"
ORACLE_SCRIPT = "/app/oracle_generator"
WRAPPER_SCRIPT = "/home/user/operator/cron_wrapper.sh"

EXPECTED_TZ = "Pacific/Fiji"
EXPECTED_LANG = "en_NZ.UTF-8"
EXPECTED_LOG_DIR = "/var/operator/manifest_logs"
EXPECTED_LOG_FILE = os.path.join(EXPECTED_LOG_DIR, "latest_manifest.yaml")
EXPECTED_POD_NAME = "system-logger-pod"

def test_generate_manifest_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Missing agent script at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def test_fuzz_equivalence_generate_manifest():
    random.seed(42)

    timezones = ["Europe/London", "America/New_York", "UTC", "Pacific/Fiji", "Asia/Tokyo"]
    locales = ["en_US.UTF-8", "fr_FR.UTF-8", "C", "en_NZ.UTF-8"]

    for _ in range(100):
        pod_name_len = random.randint(5, 20)
        pod_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=pod_name_len))
        tz = random.choice(timezones)
        lang = random.choice(locales)

        oracle_cmd = [ORACLE_SCRIPT, pod_name, tz, lang]
        agent_cmd = [AGENT_SCRIPT, pod_name, tz, lang]

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, "Oracle script failed"
        assert agent_res.returncode == 0, f"Agent script failed for inputs: {pod_name}, {tz}, {lang}"

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch for inputs: pod_name='{pod_name}', tz='{tz}', lang='{lang}'\n"
            f"Expected:\n{oracle_res.stdout}\n"
            f"Got:\n{agent_res.stdout}"
        )

def test_wrapper_script_exists_and_executable():
    assert os.path.isfile(WRAPPER_SCRIPT), f"Missing wrapper script at {WRAPPER_SCRIPT}"
    assert os.access(WRAPPER_SCRIPT, os.X_OK), f"Wrapper script at {WRAPPER_SCRIPT} is not executable"

def test_wrapper_script_execution():
    # Remove the log file if it exists to ensure the wrapper creates it
    if os.path.exists(EXPECTED_LOG_FILE):
        os.remove(EXPECTED_LOG_FILE)

    # Run the wrapper with an empty PATH
    env = {"PATH": ""}
    res = subprocess.run([WRAPPER_SCRIPT], env=env, capture_output=True, text=True)

    assert res.returncode == 0, f"Wrapper script failed with empty PATH. stderr: {res.stderr}"

    assert os.path.isdir(EXPECTED_LOG_DIR), f"Log directory {EXPECTED_LOG_DIR} was not created"
    assert os.path.isfile(EXPECTED_LOG_FILE), f"Manifest log file {EXPECTED_LOG_FILE} was not created"

    # Check the content of the generated manifest
    with open(EXPECTED_LOG_FILE, "r") as f:
        actual_content = f.read()

    oracle_res = subprocess.run([ORACLE_SCRIPT, EXPECTED_POD_NAME, EXPECTED_TZ, EXPECTED_LANG], capture_output=True, text=True)
    assert oracle_res.returncode == 0, "Oracle script failed"

    assert actual_content == oracle_res.stdout, (
        "The generated manifest from the wrapper does not match the expected output.\n"
        f"Expected:\n{oracle_res.stdout}\n"
        f"Got:\n{actual_content}"
    )