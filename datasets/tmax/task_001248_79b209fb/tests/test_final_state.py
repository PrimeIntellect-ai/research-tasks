# test_final_state.py

import os
import re
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

def compute_cer(predicted_path: str, ground_truth: str) -> float:
    with open(predicted_path, 'r') as f:
        predicted = f.read().strip().lower()

    predicted = re.sub(r'[^a-z ]', '', predicted)
    gt = re.sub(r'[^a-z ]', '', ground_truth.lower())

    dist = levenshtein_distance(predicted, gt)
    cer = dist / len(gt) if len(gt) > 0 else float('inf')
    return cer

def test_transcript_exists():
    path = "/home/user/transcript.txt"
    assert os.path.isfile(path), f"Transcript file {path} does not exist. Did you run the transcription?"

def test_transcript_accuracy():
    path = "/home/user/transcript.txt"
    assert os.path.isfile(path), f"Transcript file {path} is missing."

    ground_truth = "The system architecture requires strict modularity and scale"
    cer = compute_cer(path, ground_truth)

    threshold = 0.15
    assert cer <= threshold, f"Character Error Rate (CER) is {cer:.3f}, which is above the maximum allowed threshold of {threshold}. The transcription did not accurately match the expected audio content."