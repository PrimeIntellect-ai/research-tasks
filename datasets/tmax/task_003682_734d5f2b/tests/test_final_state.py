# test_final_state.py
import os
import subprocess
import pytest

EVIL_DIR = "/home/user/corpora/evil/"
CLEAN_DIR = "/home/user/corpora/clean/"
SCRIPT_PATH = "/home/user/jwt_scanner.py"
API_JWS_PATH = "/app/pyjwt/jwt/api_jws.py"

def test_pyjwt_perturbation_removed():
    """Ensure the deliberate backdoor in the vendored pyjwt package has been removed."""
    assert os.path.isfile(API_JWS_PATH), f"{API_JWS_PATH} is missing"
    with open(API_JWS_PATH, "r") as f:
        content = f.read()

    # Check that the specific perturbation logic is gone
    # The perturbation was: if header.get("alg") == "none": return True
    assert 'header.get("alg") == "none"' not in content.replace("'", '"'), \
        "The backdoor perturbation in api_jws.py is still present."

def test_scanner_script_exists():
    """Ensure the student created the scanner script."""
    assert os.path.isfile(SCRIPT_PATH), f"Scanner script {SCRIPT_PATH} is missing"

def test_adversarial_corpus():
    """
    Test the scanner script against the evil and clean corpora.
    Evil files must be rejected (exit code 1).
    Clean files must be accepted (exit code 0).
    """
    assert os.path.isfile(SCRIPT_PATH), f"Scanner script {SCRIPT_PATH} is missing"

    evil_files = sorted([f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))])
    clean_files = sorted([f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))])

    assert len(evil_files) > 0, "No evil corpus files found in /home/user/corpora/evil/"
    assert len(clean_files) > 0, "No clean corpus files found in /home/user/corpora/clean/"

    evil_bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        with open(filepath, "r") as f:
            token = f.read().strip()

        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--token", token],
            capture_output=True
        )
        # Evil tokens MUST be rejected (exit code 1, or at least non-zero)
        # If it exits with 0, it bypassed the security checks.
        if result.returncode == 0:
            evil_bypassed.append(filename)

    clean_modified = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, "r") as f:
            token = f.read().strip()

        result = subprocess.run(
            ["python3", SCRIPT_PATH, "--token", token],
            capture_output=True
        )
        # Clean tokens MUST be accepted (exit code 0)
        if result.returncode != 0:
            clean_modified.append(filename)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))