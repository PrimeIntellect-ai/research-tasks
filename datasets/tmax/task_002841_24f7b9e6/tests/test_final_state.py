# test_final_state.py

import os
import subprocess
import pytest

def test_patched_app_security_score():
    """
    Validates that the patched application achieves the required security score
    by running the automated grading script.
    """
    patched_app_path = "/home/user/patched_app.py"
    grader_path = "/app/grade_security.py"

    # Ensure the student created the patched file
    assert os.path.exists(patched_app_path), f"Patched app not found at {patched_app_path}. You must create the patched version."
    assert os.path.isfile(patched_app_path), f"{patched_app_path} is not a file."

    # Ensure the grader script is present
    assert os.path.exists(grader_path), f"Grader script not found at {grader_path}."

    # Run the grading script
    result = subprocess.run(
        ["python3", grader_path, patched_app_path],
        capture_output=True,
        text=True
    )

    # Check if the script executed successfully
    assert result.returncode == 0, f"Grader script failed to execute. Stderr: {result.stderr}"

    # Parse the output metric
    output = result.stdout.strip()
    try:
        score = float(output)
    except ValueError:
        pytest.fail(f"Grader script did not output a valid float. Output was: {output}")

    # Assert the score meets the threshold
    assert score >= 1.0, f"Security score is {score}, but expected >= 1.0. Check your patches for command injection, insecure cookies, and credential leaks."