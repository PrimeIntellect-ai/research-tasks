# test_final_state.py

import os
import pytest

def calculate_wer(reference: str, hypothesis: str) -> float:
    ref_words = reference.lower().split()
    hyp_words = hypothesis.lower().split()

    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(
                d[i - 1][j] + 1,        # deletion
                d[i][j - 1] + 1,        # insertion
                d[i - 1][j - 1] + cost  # substitution
            )

    if len(ref_words) == 0:
        return float('inf')
    return d[len(ref_words)][len(hyp_words)] / float(len(ref_words))

def test_skipped_log_exists_and_contains_malicious_path():
    """Verify that the skipped.log exists and contains the malicious path."""
    log_path = "/home/user/skipped.log"
    assert os.path.exists(log_path), f"The log file '{log_path}' does not exist. Did the Rust tool log skipped files?"
    assert os.path.isfile(log_path), f"'{log_path}' is not a file."

    with open(log_path, "r") as f:
        content = f.read()

    assert "../malicious_overwrite.sh" in content, (
        f"The log file '{log_path}' does not contain the expected malicious path '../malicious_overwrite.sh'. "
        "Ensure your tool detects and logs escaping paths."
    )

def test_transcript_wer_metric():
    """Verify that the transcript exists and its Word Error Rate is within the acceptable threshold."""
    transcript_path = "/home/user/transcript.txt"
    assert os.path.exists(transcript_path), f"The transcript file '{transcript_path}' does not exist."
    assert os.path.isfile(transcript_path), f"'{transcript_path}' is not a file."

    with open(transcript_path, "r") as f:
        transcript = f.read().strip()

    ground_truth = "Administrator log day forty two. The incremental backup stream has been corrupted by a path traversal payload. Manual extraction is required."

    wer = calculate_wer(ground_truth, transcript)
    threshold = 0.15

    assert wer <= threshold, (
        f"Word Error Rate (WER) is too high. "
        f"Expected <= {threshold}, got {wer:.4f}. "
        f"Transcript was: '{transcript}'"
    )