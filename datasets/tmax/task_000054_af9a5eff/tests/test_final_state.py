# test_final_state.py

import os
import pytest

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def calculate_accuracy(reference, candidate):
    distance = levenshtein_distance(reference, candidate)
    max_len = max(len(reference), len(candidate))
    if max_len == 0:
        return 1.0
    return 1.0 - (distance / max_len)

def test_extracted_payload_accuracy():
    output_path = "/home/user/extracted_payload.txt"
    assert os.path.isfile(output_path), f"Expected output file is missing at {output_path}"

    with open(output_path, 'r') as f:
        candidate = f.read().strip()

    reference = "CRITICAL_PAYLOAD_INITIATED_0x8F2A_OVERRIDE_ACTIVE"
    accuracy = calculate_accuracy(reference, candidate)

    assert accuracy >= 0.95, f"Extracted payload accuracy {accuracy:.4f} is below the threshold of 0.95. Candidate text: '{candidate}'"