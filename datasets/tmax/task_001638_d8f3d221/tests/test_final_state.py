# test_final_state.py

import os
import json
import subprocess
import pytest

CLASSIFIER_PATH = "/home/user/classifier.py"
CLEAN_CORPUS_DIR = "/app/verifier_corpus/clean"
EVIL_CORPUS_DIR = "/app/verifier_corpus/evil"
CORPUS_DIR = "/app/corpus"
FINAL_RESULT_PATH = "/home/user/final_result.json"

def test_classifier_clean_corpus():
    assert os.path.isfile(CLASSIFIER_PATH), f"Classifier script is missing at {CLASSIFIER_PATH}"

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found to test."

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(["python3", CLASSIFIER_PATH, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {failed_clean}"

def test_classifier_evil_corpus():
    assert os.path.isfile(CLASSIFIER_PATH), f"Classifier script is missing at {CLASSIFIER_PATH}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found to test."

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(["python3", CLASSIFIER_PATH, ef], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {failed_evil}"

def is_clean(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    max_valency = {'H': 1, 'O': 2, 'N': 3, 'C': 4}
    degrees = {atom['id']: 0 for atom in data.get('atoms', [])}
    for bond in data.get('bonds', []):
        degrees[bond[0]] += 1
        degrees[bond[1]] += 1

    for atom in data.get('atoms', []):
        if degrees[atom['id']] > max_valency.get(atom['element'], 0):
            return False
    return True

def test_final_result():
    assert os.path.isfile(FINAL_RESULT_PATH), f"Final result file is missing at {FINAL_RESULT_PATH}"

    with open(FINAL_RESULT_PATH, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Final result is not a valid JSON file.")

    metric = result.get("metric", "").lower().replace("_", " ")
    assert "average" in metric and "clustering" in metric and "coefficient" in metric, \
        f"Incorrect metric name: {result.get('metric')}"

    clean_count = 0
    for root, _, files in os.walk(CORPUS_DIR):
        for file in files:
            if file.endswith('.json'):
                if is_clean(os.path.join(root, file)):
                    clean_count += 1

    assert result.get("num_clean_graphs") == clean_count, \
        f"Expected {clean_count} clean graphs, got {result.get('num_clean_graphs')}"

    ci_lower = result.get("ci_lower")
    ci_upper = result.get("ci_upper")

    assert isinstance(ci_lower, (int, float)), "ci_lower must be a number"
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a number"
    assert 0 <= ci_lower <= ci_upper <= 1, f"CIs must be valid probabilities, got [{ci_lower}, {ci_upper}]"