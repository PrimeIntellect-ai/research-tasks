# test_final_state.py

import os
import pytest

def get_expected_data():
    fasta_path = "/home/user/sequence.fasta"
    if not os.path.exists(fasta_path):
        pytest.fail(f"Missing {fasta_path}")

    with open(fasta_path, 'r') as f:
        seq = ''.join(line.strip() for line in f if not line.startswith('>'))

    transitions = {}
    k = 3
    for i in range(len(seq) - k):
        k1 = seq[i:i+k]
        k2 = seq[i+1:i+1+k]
        pair = (k1, k2)
        transitions[pair] = transitions.get(pair, 0) + 1

    expected_matrix_lines = []
    for (k1, k2), count in transitions.items():
        expected_matrix_lines.append(f"{k1} -> {k2} : {count}")

    expected_matrix_lines.sort()

    sorted_transitions = sorted(transitions.items(), key=lambda x: (-x[1], x[0][0], x[0][1]))
    if sorted_transitions:
        top_k1, top_k2 = sorted_transitions[0][0]
        expected_top = f"{top_k1}-{top_k2}"
    else:
        expected_top = ""

    return expected_matrix_lines, expected_top

def test_transition_matrix():
    """Check if transition_matrix.txt is correct."""
    matrix_path = "/home/user/transition_matrix.txt"
    assert os.path.isfile(matrix_path), f"File {matrix_path} is missing."

    expected_lines, _ = get_expected_data()

    with open(matrix_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The contents of transition_matrix.txt do not match the expected sorted output."

def test_top_transition():
    """Check if top_transition.txt is correct."""
    top_path = "/home/user/top_transition.txt"
    assert os.path.isfile(top_path), f"File {top_path} is missing."

    _, expected_top = get_expected_data()

    with open(top_path, 'r') as f:
        actual_top = f.read().strip()

    assert actual_top == expected_top, f"Expected top transition '{expected_top}', but got '{actual_top}'."