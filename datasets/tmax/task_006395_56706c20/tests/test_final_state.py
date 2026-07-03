# test_final_state.py

import os
import json
import pytest
import re
from collections import Counter

def test_results_file_exists():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The output file {results_path} does not exist."

def test_results_format_and_content():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), "results.json is missing."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON.")

    assert "top_words" in data, "Missing 'top_words' in results.json"
    assert "posterior_means" in data, "Missing 'posterior_means' in results.json"
    assert "bootstrap_means" in data, "Missing 'bootstrap_means' in results.json"

    # Recompute the expected top words and posterior means
    data_path = "/home/user/data.txt"
    with open(data_path, "r") as f:
        lines = f.read().strip().split('\n')

    docs = []
    for line in lines:
        # Lowercase, remove non-alphabetic, split by whitespace
        cleaned = re.sub(r'[^a-z\s]', '', line.lower())
        tokens = [t for t in cleaned.split() if t]
        docs.append(tokens)

    all_tokens = [token for doc in docs for token in doc]
    token_counts = Counter(all_tokens)

    # Sort by frequency (descending), then alphabetically
    sorted_tokens = sorted(token_counts.items(), key=lambda x: (-x[1], x[0]))
    expected_top_words = [x[0] for x in sorted_tokens[:10]]

    assert data["top_words"] == expected_top_words, f"Expected top_words {expected_top_words}, got {data['top_words']}"

    # Recompute posterior means
    # Beta(2, 2) prior -> mean = (2 + k) / (2 + 2 + N)
    N = len(docs)
    expected_posterior_means = []
    for word in expected_top_words:
        presence_count = sum(1 for doc in docs if word in doc)
        post_mean = (2 + presence_count) / (4 + N)
        expected_posterior_means.append(round(post_mean, 4))

    assert len(data["posterior_means"]) == 10, "Expected 10 posterior means."
    for i, (actual, expected) in enumerate(zip(data["posterior_means"], expected_posterior_means)):
        assert abs(actual - expected) < 1e-3, f"Posterior mean for '{expected_top_words[i]}' expected ~{expected}, got {actual}"

    assert len(data["bootstrap_means"]) == 10, "Expected 10 bootstrap means."
    for i, (actual, expected) in enumerate(zip(data["bootstrap_means"], expected_posterior_means)):
        # The average of 1000 bootstrap posterior means should be very close to the original posterior mean
        assert abs(actual - expected) < 0.05, f"Bootstrap mean for '{expected_top_words[i]}' ({actual}) is too far from expected posterior mean ({expected})"