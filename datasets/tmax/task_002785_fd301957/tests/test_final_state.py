# test_final_state.py

import os
import json
import pytest

def test_files_exist():
    """Verify that all expected output files exist."""
    assert os.path.isfile("/app/extractor/extract_features"), "Executable /app/extractor/extract_features is missing."
    assert os.path.isfile("/app/extractor/features.bin"), "Binary file /app/extractor/features.bin is missing."
    assert os.path.isfile("/app/process.go"), "Go source file /app/process.go is missing."
    assert os.path.isfile("/app/peaks.json"), "Output file /app/peaks.json is missing."

def test_peaks_metric():
    """Evaluate the F1 score of the detected peaks against the ground truth."""
    peaks_file = "/app/peaks.json"
    assert os.path.isfile(peaks_file), f"{peaks_file} does not exist."

    with open(peaks_file, 'r') as f:
        try:
            preds = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {peaks_file} as JSON.")

    assert isinstance(preds, list), f"Expected {peaks_file} to contain a JSON array."

    truth = [500, 1200, 2400, 3100, 4800]

    try:
        pred_times = [p['time_ms'] for p in preds]
    except KeyError:
        pytest.fail("One or more objects in peaks.json is missing the 'time_ms' key.")

    tp = 0
    for t in truth:
        if any(abs(t - pt) <= 30 for pt in pred_times):
            tp += 1

    fp = len(pred_times) - tp
    fn = len(truth) - tp

    if tp == 0:
        f1 = 0.0
    else:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 score {f1:.4f} is below the threshold of 0.95. True positives: {tp}, False positives: {fp}, False negatives: {fn}."