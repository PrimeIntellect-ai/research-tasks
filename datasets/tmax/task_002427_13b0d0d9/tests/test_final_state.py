# test_final_state.py

import os
import subprocess
import pytest

def test_clean_csv_exists():
    clean_csv_path = "/home/user/data/clean.csv"
    assert os.path.exists(clean_csv_path), f"Clean dataset missing at {clean_csv_path}"
    assert os.path.isfile(clean_csv_path), f"{clean_csv_path} is not a file"
    assert os.path.getsize(clean_csv_path) > 0, f"{clean_csv_path} is empty"

def test_evaluator_score():
    clean_csv_path = "/home/user/data/clean.csv"
    evaluator_path = "/app/evaluator"

    assert os.path.exists(clean_csv_path), f"Clean dataset missing at {clean_csv_path}"
    assert os.path.exists(evaluator_path), f"Evaluator missing at {evaluator_path}"

    result = subprocess.run(
        [evaluator_path, clean_csv_path],
        capture_output=True,
        text=True,
        check=False
    )

    assert result.returncode == 0, f"Evaluator failed with return code {result.returncode}. stderr: {result.stderr}"

    output = result.stdout.strip()
    try:
        score = float(output)
    except ValueError:
        pytest.fail(f"Evaluator output could not be parsed as float. Output: {output}")

    assert score >= 0.35, f"Evaluator score {score} is below the threshold of 0.35"