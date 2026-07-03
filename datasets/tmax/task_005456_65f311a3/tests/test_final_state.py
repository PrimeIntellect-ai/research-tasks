# test_final_state.py
import os
import pytest

SCRIPT_FILE = "/home/user/clean_and_benchmark.sh"
VALID_JOINED_FILE = "/home/user/valid_joined.tsv"
BENCHMARK_REPORT_FILE = "/home/user/benchmark_report.tsv"
DATA_DIR = "/home/user/data"

def read_tsv(filepath):
    with open(filepath, 'r') as f:
        return [line.strip("\n").split("\t") for line in f if line.strip("\n")]

def is_positive_int(s):
    try:
        val = float(s)
        if val.is_integer() and val > 0:
            # strictly checking if the string represents an integer, not a float like "15.0"
            # but bash tools might format it differently, so we check if it parses to int
            # actually, age must be a positive integer.
            return int(val) > 0 and s.lstrip("-").isdigit()
    except ValueError:
        pass
    return False

def is_valid_score(s):
    try:
        val = float(s)
        return 0.0 <= val <= 1.0
    except ValueError:
        return False

def test_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"Script {SCRIPT_FILE} does not exist."

def test_valid_joined_content():
    assert os.path.isfile(VALID_JOINED_FILE), f"Output file {VALID_JOINED_FILE} does not exist."

    users = {row[0]: row[1:] for row in read_tsv(os.path.join(DATA_DIR, "users.tsv"))}
    predictions = {row[0]: row[1:] for row in read_tsv(os.path.join(DATA_DIR, "predictions.tsv"))}
    latencies = {row[0]: row[1:] for row in read_tsv(os.path.join(DATA_DIR, "latency.tsv"))}

    expected_valid_joined = []

    common_users = sorted(list(set(users.keys()) & set(predictions.keys()) & set(latencies.keys())), key=lambda x: int(x))

    for uid in common_users:
        age, country = users[uid]
        model_id, score = predictions[uid]
        latency_ms = latencies[uid][0]

        if is_positive_int(age) and is_valid_score(score) and is_positive_int(latency_ms):
            expected_valid_joined.append([uid, age, country, model_id, score, latency_ms])

    actual_valid_joined = read_tsv(VALID_JOINED_FILE)

    assert len(actual_valid_joined) == len(expected_valid_joined), f"Expected {len(expected_valid_joined)} rows in {VALID_JOINED_FILE}, but got {len(actual_valid_joined)}."

    for actual, expected in zip(actual_valid_joined, expected_valid_joined):
        assert actual == expected, f"Row mismatch in {VALID_JOINED_FILE}. Expected {expected}, got {actual}."

def test_benchmark_report_content():
    assert os.path.isfile(BENCHMARK_REPORT_FILE), f"Output file {BENCHMARK_REPORT_FILE} does not exist."

    # Recompute benchmark report from expected valid joined data
    users = {row[0]: row[1:] for row in read_tsv(os.path.join(DATA_DIR, "users.tsv"))}
    predictions = {row[0]: row[1:] for row in read_tsv(os.path.join(DATA_DIR, "predictions.tsv"))}
    latencies = {row[0]: row[1:] for row in read_tsv(os.path.join(DATA_DIR, "latency.tsv"))}

    common_users = sorted(list(set(users.keys()) & set(predictions.keys()) & set(latencies.keys())), key=lambda x: int(x))

    model_latencies = {}
    for uid in common_users:
        age, country = users[uid]
        model_id, score = predictions[uid]
        latency_ms = latencies[uid][0]

        if is_positive_int(age) and is_valid_score(score) and is_positive_int(latency_ms):
            model_latencies.setdefault(model_id, []).append(int(latency_ms))

    expected_report = []
    for model_id in sorted(model_latencies.keys()):
        avg_latency = sum(model_latencies[model_id]) / len(model_latencies[model_id])
        expected_report.append([model_id, f"{avg_latency:.2f}"])

    actual_report = read_tsv(BENCHMARK_REPORT_FILE)

    assert len(actual_report) == len(expected_report), f"Expected {len(expected_report)} rows in {BENCHMARK_REPORT_FILE}, but got {len(actual_report)}."

    for actual, expected in zip(actual_report, expected_report):
        assert actual == expected, f"Row mismatch in {BENCHMARK_REPORT_FILE}. Expected {expected}, got {actual}."