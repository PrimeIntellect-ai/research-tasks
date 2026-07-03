# test_final_state.py

import os
import pandas as pd
import pytest

def calculate_wer(reference, hypothesis):
    """
    Computes the Word Error Rate (WER) using Levenshtein distance.
    """
    r = reference.strip().split()
    h = hypothesis.strip().split()

    # Initialize matrix
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1].lower() == h[j - 1].lower():
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)] / float(len(r)) if len(r) > 0 else 1.0

def test_pipeline_script_exists():
    assert os.path.isfile('/home/user/pipeline.sh'), "/home/user/pipeline.sh is missing."

def test_word_freq_png_exists_and_valid():
    png_path = '/home/user/word_freq.png'
    assert os.path.isfile(png_path), f"{png_path} is missing. The plot_words.py script may have failed."
    assert os.path.getsize(png_path) >= 1000, f"{png_path} is too small, likely an empty or invalid plot."

def test_dataset_csv_and_wer():
    csv_path = '/home/user/dataset.csv'
    gt_path = '/app/ground_truth.txt'

    assert os.path.isfile(csv_path), f"{csv_path} is missing."
    assert os.path.isfile(gt_path), f"Ground truth file {gt_path} is missing."

    try:
        df = pd.read_csv(csv_path, names=['filename', 'text'])
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    assert len(df.columns) == 2, f"Expected 2 columns in {csv_path}, found {len(df.columns)}."

    hypothesis = " ".join(df['text'].dropna().astype(str).tolist())

    with open(gt_path, 'r') as f:
        reference = f.read().strip()

    wer_score = calculate_wer(reference, hypothesis)
    threshold = 0.3

    assert wer_score <= threshold, f"Word Error Rate (WER) is {wer_score:.4f}, which is greater than the threshold of {threshold}. The transcriptions are not accurate enough."