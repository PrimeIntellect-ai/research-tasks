# test_final_state.py

import os
import pytest

def compute_expected_optimal_primer():
    target_path = "/home/user/target.seq"
    background_path = "/home/user/background.seq"
    candidates_path = "/home/user/candidates.txt"

    if not (os.path.exists(target_path) and os.path.exists(background_path) and os.path.exists(candidates_path)):
        return None

    with open(target_path, "r") as f:
        target_seq = f.read().strip()

    with open(background_path, "r") as f:
        background_seq = f.read().strip()

    with open(candidates_path, "r") as f:
        candidates = [line.strip() for line in f if line.strip()]

    best_primer = None
    best_score = -float('inf')

    for primer in candidates:
        nt = target_seq.count(primer)
        nb = background_seq.count(primer)

        if nt <= nb:
            continue

        gc_count = primer.count('G') + primer.count('C')
        gc_percent = (gc_count / len(primer)) * 100
        penalty = abs(gc_percent - 50)

        score = (nt * 20) - (nb * 5) - penalty

        if score > best_score:
            best_score = score
            best_primer = primer
        elif score == best_score:
            if best_primer is None or primer < best_primer:
                best_primer = primer

    return best_primer, int(best_score) if best_score != -float('inf') else None

def test_optimal_primer_file_exists():
    """Test that the optimal_primer.txt file has been created."""
    assert os.path.isfile("/home/user/optimal_primer.txt"), "The file /home/user/optimal_primer.txt does not exist."

def test_optimal_primer_content():
    """Test that the optimal_primer.txt file contains the correct primer and score."""
    expected = compute_expected_optimal_primer()
    assert expected is not None, "Could not compute expected result due to missing input files."
    expected_primer, expected_score = expected

    with open("/home/user/optimal_primer.txt", "r") as f:
        content = f.read().strip()

    assert content == f"{expected_primer} {expected_score}", f"Expected '{expected_primer} {expected_score}', but found '{content}' in /home/user/optimal_primer.txt"