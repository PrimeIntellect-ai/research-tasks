# test_final_state.py

import os
import subprocess
import pytest

def test_database_exists():
    """Verify that the SQLite database was created."""
    db_path = "/home/user/subs.db"
    assert os.path.exists(db_path), f"Database file missing: {db_path}"
    assert os.path.isfile(db_path), f"Expected a file at {db_path}"
    assert os.path.getsize(db_path) > 0, f"Database file is empty: {db_path}"

def test_lqs_score_meets_threshold():
    """Run the evaluator binary and ensure the LQS score is >= 0.95."""
    db_path = "/home/user/subs.db"
    eval_bin = "/app/eval_lqs"

    assert os.path.exists(eval_bin), f"Evaluator binary missing: {eval_bin}"
    assert os.access(eval_bin, os.X_OK), f"Evaluator binary not executable: {eval_bin}"

    try:
        result = subprocess.run(
            [eval_bin, db_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Evaluator execution failed with exit code {e.returncode}. stderr: {e.stderr}")

    try:
        score = float(output)
    except ValueError:
        pytest.fail(f"Evaluator output could not be parsed as a float. Output was: {output}")

    threshold = 0.95
    assert score >= threshold, f"LQS score {score} is below the required threshold of {threshold}"

def test_final_score_file_exists():
    """Verify that the final_score.txt file was created."""
    score_file = "/home/user/final_score.txt"
    assert os.path.exists(score_file), f"Final score file missing: {score_file}"
    assert os.path.isfile(score_file), f"Expected a file at {score_file}"

    with open(score_file, "r") as f:
        content = f.read().strip()

    try:
        score = float(content)
    except ValueError:
        pytest.fail(f"Contents of {score_file} could not be parsed as a float. Content: {content}")

    threshold = 0.95
    assert score >= threshold, f"Score in {score_file} ({score}) is below the required threshold of {threshold}"