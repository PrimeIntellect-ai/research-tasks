# test_final_state.py
import os
import re
import subprocess
import pytest

def test_security_score():
    verifier_path = "/app/verifier/score.py"
    assert os.path.isfile(verifier_path), f"Verifier script missing at {verifier_path}"

    # Run the provided grading script
    result = subprocess.run(["python3", verifier_path], capture_output=True, text=True)

    # Extract the score from the output
    match = re.search(r"Score:\s*([0-9.]+)", result.stdout)
    assert match is not None, (
        f"Could not find 'Score: <value>' in verifier output.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    score = float(match.group(1))
    assert score >= 95, f"Security score is {score}, expected >= 95."

def test_rotation_complete_log():
    log_path = "/home/user/rotation_complete.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Check for a 16-character alphanumeric string (the new Redis password)
    match = re.search(r"[A-Za-z0-9]{16}", content)
    assert match is not None, (
        f"Could not find a 16-character alphanumeric password in {log_path}. "
        f"File content: {content}"
    )