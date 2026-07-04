# test_final_state.py

import os
import json
import difflib
import pytest

def test_results_json_exists():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Expected output file not found at {results_path}"
    assert os.path.isfile(results_path), f"{results_path} is not a file"

def test_semantic_similarity_threshold():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), "Cannot evaluate metric: results.json is missing."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not a valid JSON file.")

    expected = {
        "What is the status of the humidity sensors?": "The humidity sensors in sector A are showing anomalous readings",
        "How well is the visual anomaly detection model performing?": "It is now achieving 94 percent accuracy on the validation set",
        "What supplies need to be ordered?": "I need to order more nutrient solution for the hydroponics bay tomorrow"
    }

    scores = []
    for query, expected_ans in expected.items():
        expected_clean = expected_ans.lower().strip('. !?')

        user_ans = results.get(query, "")
        user_clean = str(user_ans).lower().strip('. !?')

        ratio = difflib.SequenceMatcher(None, expected_clean, user_clean).ratio()
        scores.append(ratio)

    avg_score = sum(scores) / len(scores) if scores else 0.0
    threshold = 0.80

    assert avg_score >= threshold, (
        f"Average string similarity ratio {avg_score:.4f} is below the required threshold of {threshold}. "
        f"Individual scores: {scores}"
    )