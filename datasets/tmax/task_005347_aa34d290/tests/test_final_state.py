# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/pipeline.py"), "/home/user/pipeline.py is missing."

def test_orchestrator_script_exists():
    assert os.path.isfile("/home/user/orchestrator.py"), "/home/user/orchestrator.py is missing."

def test_anonymization_f1_score():
    """
    Runs the provided verifier script which kills the orchestrator, evaluates the ingested logs
    in /app/clean_logs.db, calculates the F1 score for the masking logic, and exits with 0 
    if F1 >= 0.95.
    """
    verify_script_path = "/app/verify.py"
    assert os.path.isfile(verify_script_path), f"Verifier script {verify_script_path} is missing."

    result = subprocess.run(
        ["python3", verify_script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Anonymization metric threshold not met or verifier script failed.\n"
        f"Exit code: {result.returncode}\n"
        f"STDOUT: {result.stdout}\n"
        f"STDERR: {result.stderr}"
    )