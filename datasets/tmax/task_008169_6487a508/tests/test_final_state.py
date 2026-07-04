# test_final_state.py

import os
import json
import math

def load_vocab(path):
    vocab = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 2:
                vocab[parts[0]] = int(parts[1])
    return vocab

def load_jsonl(path):
    data = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            data[record['experiment_id']] = record
    return data

def tokenize(desc, vocab):
    words = desc.lower().split(' ')
    tokens = [vocab.get(w, 0) for w in words]
    if len(tokens) > 5:
        tokens = tokens[:5]
    else:
        tokens.extend([0] * (5 - len(tokens)))
    return tokens

def test_report_json_exists():
    assert os.path.isfile("/home/user/report.json"), "/home/user/report.json does not exist."

def test_report_contents():
    vocab = load_vocab("/home/user/data/vocab.txt")
    experiments = load_jsonl("/home/user/data/experiments.jsonl")
    metrics = load_jsonl("/home/user/data/metrics.jsonl")

    joined_keys = sorted(list(set(experiments.keys()).intersection(set(metrics.keys()))))

    expected_results = []
    total_squared_error = 0.0

    for exp_id in joined_keys:
        exp = experiments[exp_id]
        met = metrics[exp_id]

        tokens = tokenize(exp['desc'], vocab)
        weights = met['weights']

        score = sum(t * w for t, w in zip(tokens, weights))
        expected_results.append({
            "experiment_id": exp_id,
            "computed_score": score
        })

        error = score - exp['baseline_score']
        total_squared_error += error * error

    expected_mse = total_squared_error / len(joined_keys) if joined_keys else 0.0

    with open("/home/user/report.json", 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/report.json is not valid JSON."

    assert "mse" in report, "Report missing 'mse' field."
    assert "average_inference_ns" in report, "Report missing 'average_inference_ns' field."
    assert "results" in report, "Report missing 'results' field."

    assert isinstance(report["average_inference_ns"], (int, float)), "'average_inference_ns' must be a number."
    assert report["average_inference_ns"] >= 0, "'average_inference_ns' cannot be negative."

    assert math.isclose(report["mse"], expected_mse, rel_tol=1e-5), f"Expected MSE ~{expected_mse}, got {report['mse']}"

    assert len(report["results"]) == len(expected_results), f"Expected {len(expected_results)} results, got {len(report['results'])}"

    for i, (expected, actual) in enumerate(zip(expected_results, report["results"])):
        assert actual.get("experiment_id") == expected["experiment_id"], f"Result {i} expected experiment_id {expected['experiment_id']}, got {actual.get('experiment_id')}"
        assert "computed_score" in actual, f"Result {i} missing 'computed_score'"
        assert math.isclose(actual["computed_score"], expected["computed_score"], rel_tol=1e-5), f"Result {i} expected computed_score ~{expected['computed_score']}, got {actual['computed_score']}"