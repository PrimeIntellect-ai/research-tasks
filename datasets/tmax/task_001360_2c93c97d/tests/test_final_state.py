# test_final_state.py

import os
import json

def test_pagerank_mse():
    pred_file = '/home/user/pagerank.json'
    truth_file = '/tmp/reference_pagerank.json'

    assert os.path.isfile(pred_file), f"Output file {pred_file} is missing. The pipeline may not have run successfully."
    assert os.path.isfile(truth_file), f"Reference file {truth_file} is missing."

    try:
        with open(pred_file) as f:
            pred = json.load(f)
    except json.JSONDecodeError:
        assert False, f"Output file {pred_file} is not valid JSON."

    with open(truth_file) as f:
        truth = json.load(f)

    assert pred, "Predicted PageRank JSON is empty."
    assert truth, "Reference PageRank JSON is empty."

    keys = set(pred.keys()).union(set(truth.keys()))
    assert len(keys) > 0, "No keys found in either JSON."

    mse = sum((pred.get(k, 0.0) - truth.get(k, 0.0))**2 for k in keys) / len(keys)

    assert mse <= 0.0001, f"MSE {mse} exceeds the allowed threshold of 0.0001. The generated graph edges might be incorrect."