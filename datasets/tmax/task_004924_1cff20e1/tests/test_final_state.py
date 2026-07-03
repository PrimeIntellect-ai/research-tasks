# test_final_state.py

import os
import sys
import subprocess
import re
import pytest

def test_security_score_metric():
    """
    Run the automated testing tool and verify the security score metric is 100.
    """
    cmd = ["python3", "/app/tester/run_tests.py", "--score-only"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Testing script failed to run: {e.stderr}")

    try:
        score = float(output)
    except ValueError:
        pytest.fail(f"Testing script did not output a numeric score. Output was: {output}")

    assert score >= 100, f"Expected security score >= 100, but got {score}"

def test_valid_tokens_count():
    """
    Recompute the number of valid tokens from the access log and compare
    with the agent's output.
    """
    log_path = "/app/logs/access.log"
    output_path = "/home/user/valid_tokens_count.txt"

    assert os.path.isfile(log_path), f"Log file missing at {log_path}"
    assert os.path.isfile(output_path), f"Agent output file missing at {output_path}"

    # Add the vendored (and now fixed) PyJWT to sys.path to verify tokens
    vendored_path = "/app/pyjwt-2.4.0/"
    if vendored_path not in sys.path:
        sys.path.insert(0, vendored_path)

    try:
        import jwt
    except ImportError:
        pytest.fail("Failed to import vendored jwt library.")

    secret_key = "supersecret_key_123"
    valid_count = 0

    # Regex to extract tokens from Authorization header or token= URL parameter
    token_pattern = re.compile(r'(?:Authorization:\s*Bearer\s+|token=)([A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]*)')

    with open(log_path, "r") as f:
        for line in f:
            matches = token_pattern.findall(line)
            for token in matches:
                try:
                    # Attempt to decode and validate the token
                    jwt.decode(token, secret_key, algorithms=["HS256"])
                    valid_count += 1
                except Exception:
                    # Invalid, expired, wrong signature, or rejected 'none' alg
                    pass

    with open(output_path, "r") as f:
        agent_output = f.read().strip()

    try:
        agent_count = int(agent_output)
    except ValueError:
        pytest.fail(f"Agent output in {output_path} is not a valid integer: '{agent_output}'")

    assert agent_count == valid_count, (
        f"Agent's valid token count ({agent_count}) does not match the actual valid token count ({valid_count})."
    )

def test_file_permissions():
    """
    Verify that the permissions for the logs directory and access.log are correctly secured.
    """
    log_dir = "/app/logs"
    log_file = "/app/logs/access.log"

    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist"
    assert os.path.isfile(log_file), f"File {log_file} does not exist"

    dir_stat = os.stat(log_dir)
    file_stat = os.stat(log_file)

    # Check directory permissions (700 -> 0o700)
    dir_perms = oct(dir_stat.st_mode & 0o777)
    assert dir_perms == oct(0o700), f"Expected {log_dir} permissions to be 0o700, got {dir_perms}"

    # Check file permissions (600 -> 0o600)
    file_perms = oct(file_stat.st_mode & 0o777)
    assert file_perms == oct(0o600), f"Expected {log_file} permissions to be 0o600, got {file_perms}"