# test_final_state.py
import os
import json
import math
import pytest

def test_ml_data_stats():
    json_path = "/home/user/ml_data_stats.json"
    fasta_path = "/home/user/raw_sequences.fasta"

    assert os.path.exists(json_path), f"Expected output file {json_path} does not exist."
    assert os.path.exists(fasta_path), f"Input file {fasta_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    required_keys = {"extracted_count", "mean_gc", "ci_lower", "ci_upper"}
    assert required_keys.issubset(data.keys()), f"JSON missing required keys. Expected {required_keys}, found {list(data.keys())}"

    extracted_gcs = []
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq = line.strip()
            start = seq.find("GACCAT")
            if start != -1:
                end = seq.find("TGTCGA", start + 6)
                if end != -1:
                    sub = seq[start+6:end]
                    if len(sub) > 0:
                        gc = (sub.count("G") + sub.count("C")) / len(sub)
                        extracted_gcs.append(gc)

    exact_count = len(extracted_gcs)
    exact_mean = sum(extracted_gcs) / exact_count if exact_count > 0 else 0

    assert data['extracted_count'] == exact_count, f"Expected extracted_count {exact_count}, got {data['extracted_count']}"
    assert math.isclose(data['mean_gc'], exact_mean, rel_tol=1e-3), f"Expected mean_gc ~{exact_mean}, got {data['mean_gc']}"

    ci_lower = data['ci_lower']
    ci_upper = data['ci_upper']

    assert ci_lower < exact_mean, f"ci_lower ({ci_lower}) should be less than mean ({exact_mean})"
    assert ci_upper > exact_mean, f"ci_upper ({ci_upper}) should be greater than mean ({exact_mean})"

    ci_width = ci_upper - ci_lower
    assert ci_width < 0.1, f"Confidence interval too wide: {ci_width}. Expected < 0.1 for this sample size."
    assert ci_width > 0.01, f"Confidence interval too narrow: {ci_width}. Expected > 0.01 for this sample size."