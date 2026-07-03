# test_final_state.py

import os
import re
import subprocess
import pytest

def test_venv_and_numpy():
    """Verify that the virtual environment exists and numpy is installed."""
    python_path = "/home/user/venv/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment Python not found at {python_path}"
    assert os.access(python_path, os.X_OK), f"Python at {python_path} is not executable"

    # Check if numpy is installed
    try:
        subprocess.run(
            [python_path, "-c", "import numpy"],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError:
        pytest.fail("numpy is not installed in the virtual environment at /home/user/venv")

def test_scorer_executable():
    """Verify that the scorer executable is compiled and executable."""
    scorer_path = "/home/user/motif_project/scorer"
    assert os.path.isfile(scorer_path), f"Compiled executable not found at {scorer_path}"
    assert os.access(scorer_path, os.X_OK), f"File at {scorer_path} is not executable"

def test_optimized_sequence_file():
    """Verify the optimized sequence file exists, has correct format, and meets the score threshold."""
    result_file = "/home/user/motif_project/optimized_sequence.txt"
    assert os.path.isfile(result_file), f"Output file not found at {result_file}"

    with open(result_file, "r") as f:
        content = f.read().strip()

    lines = content.split('\n')

    seq_line = [l for l in lines if l.startswith("Sequence:")]
    assert len(seq_line) == 1, "File must contain exactly one line starting with 'Sequence:'"
    seq = seq_line[0].split("Sequence:")[1].strip()

    score_line = [l for l in lines if l.startswith("Score:")]
    assert len(score_line) == 1, "File must contain exactly one line starting with 'Score:'"

    # Check sequence properties
    assert len(seq) == 50, f"Sequence length is {len(seq)}, expected exactly 50."
    assert all(c in 'ACGT' for c in seq), f"Sequence contains invalid characters: {seq}"

    # Calculate score using the same logic as scorer.c
    score = 0
    for i in range(len(seq) - 2):
        if seq[i:i+3] == 'ATG': score += 15
    for i in range(len(seq) - 1):
        if seq[i:i+2] == 'CG': score += 7
        if seq[i:i+2] == 'GC': score += 5
        if seq[i:i+2] == 'TA': score -= 5
        if seq[i:i+2] == 'TT': score -= 3

    assert score >= 150, f"Calculated score is {score}, expected >= 150."

    # Check if the reported score matches the calculated score
    reported_score_str = score_line[0].split("Score:")[1].strip()
    try:
        reported_score = int(reported_score_str)
    except ValueError:
        pytest.fail(f"Reported score '{reported_score_str}' is not an integer.")

    assert reported_score == score, f"Reported score {reported_score} does not match actual calculated score {score}."