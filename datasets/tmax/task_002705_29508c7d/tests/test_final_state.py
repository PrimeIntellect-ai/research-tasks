# test_final_state.py
import os
import pytest

def calculate_score(fwd, rev):
    """Calculates the simplistic deterministic pseudo-efficiency score."""
    def calc_tm(seq):
        return 2 * (seq.count('A') + seq.count('T')) + 4 * (seq.count('G') + seq.count('C'))

    if len(fwd) != 20 or len(rev) != 20: 
        return 0.0
    if calc_tm(fwd) != 60 or calc_tm(rev) != 60: 
        return 0.0

    # Base score
    score = 0.5
    # Bonus for GC clamp
    if fwd[-1] in 'GC': 
        score += 0.2
    if rev[-1] in 'GC': 
        score += 0.2

    return min(1.0, score)

def test_primer_efficiency_score():
    """Validates that the output file exists and the primer pair achieves an efficiency score >= 0.85."""
    output_file = "/home/user/best_primers.txt"

    assert os.path.exists(output_file), f"Output file not found: {output_file}"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert ',' in content, f"Output file {output_file} does not contain comma-separated primers. Content: '{content}'"

    parts = content.split(',')
    assert len(parts) == 2, f"Output file {output_file} must contain exactly two comma-separated strings."

    fwd, rev = parts[0].strip(), parts[1].strip()

    score = calculate_score(fwd, rev)
    threshold = 0.85

    assert score >= threshold, (
        f"Efficiency score for primers ({fwd}, {rev}) is {score}, "
        f"which is below the required threshold of {threshold}."
    )