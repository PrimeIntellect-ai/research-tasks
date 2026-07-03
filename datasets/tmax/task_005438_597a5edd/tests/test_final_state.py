# test_final_state.py
import os
import subprocess
import pytest

def test_solution_format_and_score():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"Solution file {solution_path} does not exist."
    assert os.path.isfile(solution_path), f"Path {solution_path} is not a file."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content, "Solution file is empty."
    parts = content.split(",")
    assert len(parts) == 2, f"Solution file must contain exactly one line in format SEQUENCE,SCORE. Found: {content}"

    seq, score_str = parts
    seq = seq.strip()

    assert len(seq) == 20, f"Sequence must be exactly 20 bp long. Found length {len(seq)}: {seq}"
    assert all(c in "ACGT" for c in seq), f"Sequence contains invalid characters. Must be A, C, G, T only. Found: {seq}"

    scorer_path = "/app/binding_scorer"
    assert os.path.exists(scorer_path) and os.access(scorer_path, os.X_OK), f"Scorer binary {scorer_path} is missing or not executable."

    result = subprocess.run([scorer_path, seq], capture_output=True, text=True)
    assert result.returncode == 0, f"Scorer binary failed with return code {result.returncode}. stderr: {result.stderr}"

    try:
        score = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Could not parse score from scorer output: {result.stdout}")

    threshold = 85.0
    assert score >= threshold, f"Binding affinity score {score} is below the threshold of {threshold}."