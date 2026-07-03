# test_final_state.py

import os
import json
import subprocess
import pytest

def calculate_wer(reference, hypothesis):
    """Calculate Word Error Rate (WER) using Levenshtein distance at the word level."""
    r = reference.split()
    h = hypothesis.split()
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]

    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
            else:
                if r[i - 1] == h[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    d[i][j] = 1 + min(
                        d[i - 1][j],      # deletion
                        d[i][j - 1],      # insertion
                        d[i - 1][j - 1]   # substitution
                    )

    if len(r) == 0:
        return float('inf')
    return d[len(r)][len(h)] / len(r)

def test_transcription_accuracy():
    """
    Test that the transcription accuracy (1.0 - WER) is >= 0.85.
    """
    ground_truth = "the mathematical foundations of data engineering require careful attention to timestamp alignment and rigorous data stratification when building an etl pipeline one must normalize incoming tokens effectively"
    target_file = "/home/user/full_transcript.txt"

    assert os.path.exists(target_file), f"Transcript file missing: {target_file}"

    with open(target_file, "r") as f:
        predicted = f.read().strip()

    error = calculate_wer(ground_truth, predicted)
    accuracy = max(0.0, 1.0 - error)

    assert accuracy >= 0.85, f"Transcription accuracy is {accuracy:.2f}, which is below the threshold of 0.85."

def test_cron_job_configured():
    """
    Test that the cron job is configured to run at 04:30 AM every day.
    """
    try:
        cron_check = subprocess.check_output(["crontab", "-l"], stderr=subprocess.DEVNULL).decode("utf-8")
    except subprocess.CalledProcessError:
        cron_check = ""

    assert "30 4 * * *" in cron_check, "Cron job is not configured correctly. Expected '30 4 * * *' in crontab."

def test_stratified_sample():
    """
    Test that the stratified sample is a JSON array of exactly 30 words.
    """
    sample_file = "/home/user/stratified_sample.json"
    assert os.path.exists(sample_file), f"Stratified sample file missing: {sample_file}"

    with open(sample_file, "r") as f:
        try:
            sample = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Stratified sample file is not valid JSON.")

    assert isinstance(sample, list), "Stratified sample must be a JSON array."
    assert len(sample) == 30, f"Stratified sample must contain exactly 30 words, found {len(sample)}."
    assert all(isinstance(word, str) for word in sample), "All items in the stratified sample must be strings."