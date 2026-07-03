# test_final_state.py
import os
import subprocess
import hashlib
import re
import pytest

def test_app_secure_binary():
    """Test that the compiled binary exists, uses DB_PASSWORD, and rejects --password."""
    bin_path = "/home/user/app_secure"
    assert os.path.isfile(bin_path), f"Binary not found: {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Binary is not executable: {bin_path}"

    password = "N3wR0D4tionPass!2024"
    expected_hash = hashlib.sha256(password.encode()).hexdigest()

    env = os.environ.copy()
    env["DB_PASSWORD"] = password

    # Test valid execution using DB_PASSWORD
    result = subprocess.run([bin_path, "--username=admin"], env=env, capture_output=True, text=True)
    assert expected_hash in result.stdout, "App did not output the expected hash using the DB_PASSWORD environment variable."

    # Test that --password flag is no longer accepted
    result_fail = subprocess.run([bin_path, "--password=secret"], env=env, capture_output=True, text=True)
    assert result_fail.returncode != 0, "App should fail when the removed --password flag is provided."
    output = result_fail.stderr + result_fail.stdout
    assert "provided but not defined" in output or "flag provided but not defined: -password" in output, \
        "App did not fail with the expected flag parsing error for --password."

def test_id_rule():
    """Test that the regex rule correctly matches --password with non-whitespace characters."""
    rule_path = "/home/user/id_rule.txt"
    assert os.path.isfile(rule_path), f"File not found: {rule_path}"

    with open(rule_path, "r") as f:
        regex_str = f.read().strip()

    assert regex_str, "Regex file is empty."

    try:
        pattern = re.compile(regex_str)
    except re.error as e:
        pytest.fail(f"Invalid regex compiled: {e}")

    assert pattern.search("./app --password=secret123"), "Regex failed to match a valid target (e.g. --password=secret123)."
    assert not pattern.search("./app --password="), "Regex incorrectly matched an empty password (--password=)."
    assert not pattern.search("./app --password= "), "Regex incorrectly matched a password with only whitespace (--password= )."

def test_rotation_summary():
    """Test that the rotation summary contains the correct CWE and decoded password."""
    summary_path = "/home/user/rotation_summary.txt"
    assert os.path.isfile(summary_path), f"File not found: {summary_path}"

    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines()]

    assert len(lines) >= 2, "Summary file must have at least two lines."

    cwe = lines[0]
    assert "CWE-214" in cwe or "CWE-314" in cwe, f"Line 1 does not contain the correct CWE (expected CWE-214 or CWE-314). Found: {cwe}"

    password = lines[1]
    assert password == "N3wR0D4tionPass!2024", f"Line 2 does not contain the correct decoded password. Found: {password}"