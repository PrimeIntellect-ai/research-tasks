# test_final_state.py

import os
import subprocess
import pytest

def test_cert_status_verified():
    status_file = "/home/user/cert_status.txt"
    assert os.path.exists(status_file), f"File {status_file} is missing. Did you perform the integrity verification?"

    with open(status_file, "r") as f:
        content = f.read().strip()

    assert content == "VERIFIED", f"Expected {status_file} to contain 'VERIFIED', but found '{content}'."

def test_legacy_runner_execution_and_log():
    runner_script = "/home/user/legacy_runner.sh"
    log_file = "/home/user/processing.log"

    # Ensure the log file is removed before running to verify it's recreated properly
    if os.path.exists(log_file):
        os.remove(log_file)

    # Execute the runner script
    result = subprocess.run(["bash", runner_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {runner_script} failed with error: {result.stderr}"

    assert os.path.exists(log_file), f"Log file {log_file} was not created after running the script."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "[REDACTED]" in log_content, f"The log file {log_file} does not contain the redacted string '[REDACTED]'."
    assert "SUPER_SECRET_99!" not in log_content, f"The log file {log_file} still contains the plaintext password!"

def test_legacy_runner_content():
    runner_script = "/home/user/legacy_runner.sh"
    assert os.path.exists(runner_script), f"File {runner_script} is missing."

    with open(runner_script, "r") as f:
        content = f.read()

    assert "--db-pass" not in content, f"The script {runner_script} still passes '--db-pass' as a command-line argument."
    assert "DB_PASSWORD" in content, f"The script {runner_script} does not seem to set the 'DB_PASSWORD' environment variable."
    assert "SUPER_SECRET_99!" in content, f"The script {runner_script} is missing the actual password value."

def test_processor_content():
    processor_script = "/home/user/processor.py"
    assert os.path.exists(processor_script), f"File {processor_script} is missing."

    with open(processor_script, "r") as f:
        content = f.read()

    assert "--db-pass" not in content, f"The script {processor_script} still defines or uses the '--db-pass' argument."

    # Check if os.environ or os.getenv is used for DB_PASSWORD
    uses_env = "os.environ" in content or "os.getenv" in content
    assert uses_env, f"The script {processor_script} does not appear to read from the environment (missing os.environ or os.getenv)."
    assert "DB_PASSWORD" in content, f"The script {processor_script} does not reference the 'DB_PASSWORD' environment variable."