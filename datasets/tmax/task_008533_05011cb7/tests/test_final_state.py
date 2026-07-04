# test_final_state.py
import os
import csv
import json
import math
import pytest

def get_stats(data):
    n = len(data)
    if n == 0:
        return 0, 0, 0
    mean = sum(data) / n
    if n == 1:
        return n, mean, 0
    var = sum((x - mean) ** 2 for x in data) / (n - 1)
    return n, mean, var

def test_clean_data_csv():
    file_path = "/home/user/clean_data.csv"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 383, f"Expected exactly 383 valid records in clean_data.csv, found {len(rows)}."

    for i, row in enumerate(rows):
        tid = row.get('ticket_id', '')
        assert tid, f"Missing ticket_id at row {i+1}"
        assert '.' not in tid, f"ticket_id '{tid}' appears to be a float. It must be an integer."
        assert row.get('label') in ('bug', 'feature'), f"Unexpected label '{row.get('label')}' at row {i+1}."

def test_results_json():
    json_path = "/home/user/results.json"
    csv_path = "/home/user/clean_data.csv"

    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    required_keys = {
        "num_valid_records",
        "mean_tokens_bug",
        "mean_tokens_feature",
        "t_statistic",
        "p_value"
    }
    assert required_keys.issubset(results.keys()), f"Missing keys in results.json. Found: {list(results.keys())}"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    bug_lengths = [len(r['text'].split()) for r in rows if r['label'] == 'bug']
    feature_lengths = [len(r['text'].split()) for r in rows if r['label'] == 'feature']

    n1, m1, v1 = get_stats(bug_lengths)
    n2, m2, v2 = get_stats(feature_lengths)

    expected_t = (m1 - m2) / math.sqrt(v1/n1 + v2/n2)

    assert results['num_valid_records'] == len(rows), \
        f"num_valid_records should be {len(rows)}, got {results['num_valid_records']}."

    assert math.isclose(results['mean_tokens_bug'], round(m1, 2), abs_tol=0.01), \
        f"mean_tokens_bug mismatch. Expected ~{round(m1, 2)}, got {results['mean_tokens_bug']}."

    assert math.isclose(results['mean_tokens_feature'], round(m2, 2), abs_tol=0.01), \
        f"mean_tokens_feature mismatch. Expected ~{round(m2, 2)}, got {results['mean_tokens_feature']}."

    assert math.isclose(abs(results['t_statistic']), abs(round(expected_t, 2)), abs_tol=0.02), \
        f"t_statistic mismatch. Expected ~{round(expected_t, 2)}, got {results['t_statistic']}."

    assert isinstance(results['p_value'], (int, float)), "p_value must be a number."
    assert 0 <= results['p_value'] <= 1, "p_value must be between 0 and 1."