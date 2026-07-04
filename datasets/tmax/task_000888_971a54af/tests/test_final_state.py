# test_final_state.py

import os
import math
import re
import pytest

def calculate_score(seq, primer):
    max_score = -len(primer)
    for i in range(len(seq) - len(primer) + 1):
        window = seq[i:i+len(primer)]
        matches = sum(1 for a, b in zip(window, primer) if a == b)
        mismatches = len(primer) - matches
        score = matches - mismatches
        if score > max_score:
            max_score = score
    return max_score

def get_scores(fasta_path, primer):
    scores = []
    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('>'):
                scores.append(calculate_score(line, primer))
    return scores

def calc_stats(scores_A, scores_B):
    mean_A = sum(scores_A) / len(scores_A)
    mean_B = sum(scores_B) / len(scores_B)

    var_A = sum((x - mean_A)**2 for x in scores_A) / (len(scores_A) - 1) if len(scores_A) > 1 else 0
    var_B = sum((x - mean_B)**2 for x in scores_B) / (len(scores_B) - 1) if len(scores_B) > 1 else 0

    t_stat = (mean_A - mean_B) / math.sqrt(var_A / len(scores_A) + var_B / len(scores_B))
    return mean_A, mean_B, t_stat

def test_makefile_and_executable_exist():
    """Test that the Makefile and compiled executable exist."""
    makefile_path = "/home/user/Makefile"
    executable_path = "/home/user/primer_test"

    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_analysis_result_exists():
    """Test that the analysis_result.txt file exists."""
    result_path = "/home/user/analysis_result.txt"
    assert os.path.isfile(result_path), f"Output file not found at {result_path}"

def test_analysis_result_content():
    """Test that the analysis_result.txt contains the correct computed values."""
    pop_a_path = "/home/user/pop_A.fasta"
    pop_b_path = "/home/user/pop_B.fasta"
    result_path = "/home/user/analysis_result.txt"
    primer = "ATGCGTACG"

    # Recompute expected values
    scores_A = get_scores(pop_a_path, primer)
    scores_B = get_scores(pop_b_path, primer)
    expected_mean_A, expected_mean_B, expected_t_stat = calc_stats(scores_A, scores_B)

    # Read actual values
    with open(result_path, 'r') as f:
        content = f.read()

    match_A = re.search(r"Mean A:\s*([-\d.]+)", content)
    match_B = re.search(r"Mean B:\s*([-\d.]+)", content)
    match_t = re.search(r"t-statistic:\s*([-\d.]+)", content)

    assert match_A is not None, "Could not find 'Mean A: [value]' in analysis_result.txt"
    assert match_B is not None, "Could not find 'Mean B: [value]' in analysis_result.txt"
    assert match_t is not None, "Could not find 't-statistic: [value]' in analysis_result.txt"

    actual_mean_A = float(match_A.group(1))
    actual_mean_B = float(match_B.group(1))
    actual_t_stat = float(match_t.group(1))

    # Compare with tolerance
    assert actual_mean_A == pytest.approx(expected_mean_A, abs=1e-3), f"Mean A is incorrect. Expected {expected_mean_A:.4f}, got {actual_mean_A}"
    assert actual_mean_B == pytest.approx(expected_mean_B, abs=1e-3), f"Mean B is incorrect. Expected {expected_mean_B:.4f}, got {actual_mean_B}"
    assert actual_t_stat == pytest.approx(expected_t_stat, abs=1e-3), f"t-statistic is incorrect. Expected {expected_t_stat:.4f}, got {actual_t_stat}"