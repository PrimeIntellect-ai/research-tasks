# test_final_state.py

import os
import pytest

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def test_final_transcript_levenshtein_distance():
    file_path = "/home/user/final_transcript.txt"
    assert os.path.isfile(file_path), f"Final transcript file not found at {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    ground_truth = "The quick brown fox jumps over the lazy dog, but the dog was not amused."

    distance = levenshtein_distance(content, ground_truth)
    threshold = 5

    assert distance <= threshold, (
        f"Levenshtein distance is {distance}, which is greater than the threshold {threshold}.\n"
        f"Expected: '{ground_truth}'\n"
        f"Got: '{content}'"
    )