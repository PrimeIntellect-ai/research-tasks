# test_final_state.py
import os
import pytest

def levenshtein_distance(s1: str, s2: str) -> int:
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

def test_extracted_text_metric():
    target_file = '/home/user/extracted.txt'
    assert os.path.exists(target_file), f"Expected extracted text file not found at {target_file}"

    with open(target_file, 'r', encoding='utf-8') as f:
        extracted = f.read().strip()

    truth = """INVOICE #9981
Date: 2023-10-01
Total: $1,234.56
Thank you for your business!"""

    distance = levenshtein_distance(truth.strip(), extracted)

    assert distance <= 10, f"Levenshtein distance is {distance}, which exceeds the threshold of 10. Extracted text was:\n{extracted}"