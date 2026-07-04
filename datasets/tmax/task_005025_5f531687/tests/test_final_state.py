# test_final_state.py

import os
import re
import pytest

def test_source_code_exists():
    assert os.path.isfile("/home/user/analyze_motifs.c"), "C source file /home/user/analyze_motifs.c is missing."

def test_results_file_exists():
    assert os.path.isfile("/home/user/motif_results.txt"), "Results file /home/user/motif_results.txt is missing."

def test_results_content():
    with open("/home/user/motif_results.txt", "r") as f:
        content = f.read().strip()

    # Expected format:
    # Smoothed Sigma1: [Value]
    # Bootstrap 95% CI: [[Lower], [Upper]]

    sigma1_match = re.search(r"Smoothed Sigma1:\s*([0-9.]+)", content)
    assert sigma1_match is not None, "Could not find 'Smoothed Sigma1: [Value]' in the results file."

    ci_match = re.search(r"Bootstrap 95% CI:\s*\[([0-9.]+),\s*([0-9.]+)\]", content)
    assert ci_match is not None, "Could not find 'Bootstrap 95% CI: [[Lower], [Upper]]' in the results file."

    sigma1 = float(sigma1_match.group(1))
    lower = float(ci_match.group(1))
    upper = float(ci_match.group(2))

    assert 44.4924 <= sigma1 <= 44.4926, f"Smoothed Sigma1 {sigma1} is out of expected range [44.4924, 44.4926]."
    assert 38.2 <= lower <= 40.5, f"Bootstrap CI Lower bound {lower} is out of expected range [38.2, 40.5]."
    assert 48.5 <= upper <= 50.5, f"Bootstrap CI Upper bound {upper} is out of expected range [48.5, 50.5]."