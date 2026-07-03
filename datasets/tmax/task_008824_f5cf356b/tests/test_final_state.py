# test_final_state.py

import os
import json
import math
import pytest

def compute_expected_mean_similarity():
    raw_data_dir = '/home/user/raw_data'
    files = sorted(os.listdir(raw_data_dir))
    docs = []
    vocab = set()
    for f in files:
        with open(os.path.join(raw_data_dir, f), 'r') as file:
            text = file.read().lower()
            for p in ['.', ',', '!', '?']:
                text = text.replace(p, '')
            tokens = text.split()
            docs.append(tokens)
            vocab.update(tokens)

    vocab = sorted(list(vocab))
    vocab_idx = {w: i for i, w in enumerate(vocab)}

    # Vectorize
    TF = [[0] * len(vocab) for _ in range(len(docs))]
    for i, tokens in enumerate(docs):
        for token in tokens:
            TF[i][vocab_idx[token]] += 1

    # Cosine similarity
    norms = []
    for row in TF:
        norm = math.sqrt(sum(x * x for x in row))
        norms.append(norm if norm > 0 else 1.0)

    TF_norm = []
    for i, row in enumerate(TF):
        TF_norm.append([x / norms[i] for x in row])

    pairwise_sims = []
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            sim = sum(TF_norm[i][k] * TF_norm[j][k] for k in range(len(vocab)))
            pairwise_sims.append(sim)

    mean_sim = sum(pairwise_sims) / len(pairwise_sims)
    return round(mean_sim, 4)

def test_output_file_exists():
    output_path = '/home/user/etl_output.json'
    assert os.path.exists(output_path), f"Expected output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_output_file_content():
    output_path = '/home/user/etl_output.json'
    assert os.path.exists(output_path), "Output file missing."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    expected_keys = {"mean_similarity", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected. Found {list(data.keys())}, expected {list(expected_keys)}"

    for key in expected_keys:
        assert isinstance(data[key], float), f"Value for {key} should be a float, got {type(data[key])}."

    expected_mean = compute_expected_mean_similarity()
    assert math.isclose(data["mean_similarity"], expected_mean, rel_tol=1e-4), \
        f"mean_similarity is incorrect. Expected ~{expected_mean}, got {data['mean_similarity']}."

    assert data["ci_lower"] <= data["mean_similarity"], "ci_lower should be less than or equal to mean_similarity."
    assert data["ci_upper"] >= data["mean_similarity"], "ci_upper should be greater than or equal to mean_similarity."
    assert data["ci_lower"] < data["ci_upper"], "ci_lower should be strictly less than ci_upper."