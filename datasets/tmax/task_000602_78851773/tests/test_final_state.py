# test_final_state.py

import os
import subprocess
import re
import pytest

def test_pipeline_script_exists():
    path = "/home/user/clean_pipeline.sh"
    assert os.path.exists(path), f"Missing pipeline script: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_cleaned_chats_exists():
    path = "/home/user/cleaned_chats.txt"
    assert os.path.exists(path), f"Missing cleaned output file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_evaluator_score():
    output_file = "/home/user/cleaned_chats.txt"
    evaluator_path = "/app/evaluator"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.exists(evaluator_path), f"Evaluator binary {evaluator_path} does not exist."
    assert os.access(evaluator_path, os.X_OK), f"Evaluator binary {evaluator_path} is not executable."

    try:
        result = subprocess.run(
            [evaluator_path, output_file],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Evaluator failed to run. Return code: {e.returncode}\nStdout: {e.stdout}\nStderr: {e.stderr}")

    output = result.stdout.strip()

    # Extract score, expecting format like "Score: 0.98"
    match = re.search(r"Score:\s*([0-9]*\.?[0-9]+)", output)
    assert match is not None, f"Could not find score in evaluator output. Output was:\n{output}"

    score = float(match.group(1))
    threshold = 0.95

    assert score >= threshold, f"Data Readiness Score {score} is below the required threshold of {threshold}."