# test_final_state.py

import os
import csv
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/process_pipeline.sh"
    assert os.path.exists(script_path), f"Pipeline script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script is not executable: {script_path}"

def test_candidate_scores_mse():
    candidate_path = "/home/user/candidate_scores.csv"
    truth_path = "/app/ground_truth.csv"

    assert os.path.exists(candidate_path), f"Output file missing: {candidate_path}"
    assert os.path.exists(truth_path), f"Ground truth file missing: {truth_path}"

    # Read ground truth
    truth_scores = {}
    with open(truth_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == "Sequence_ID":
                continue
            seq_id, score = row[0], float(row[1])
            truth_scores[seq_id] = score

    # Read candidate scores
    candidate_scores = {}
    with open(candidate_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == "Sequence_ID":
                continue
            seq_id, score = row[0], float(row[1])
            candidate_scores[seq_id] = score

    assert len(candidate_scores) > 0, "Candidate scores file is empty or invalid"
    assert set(candidate_scores.keys()) == set(truth_scores.keys()), "Candidate sequence IDs do not match ground truth sequence IDs"

    # Calculate MSE
    squared_errors = []
    for seq_id in truth_scores:
        diff = candidate_scores[seq_id] - truth_scores[seq_id]
        squared_errors.append(diff ** 2)

    mse = sum(squared_errors) / len(squared_errors)
    threshold = 0.01

    assert mse <= threshold, f"MSE of Alignment Scores is {mse:.6f}, which exceeds the threshold of {threshold}"