# test_final_state.py

import os
import json
import csv
import math

def test_venv_exists():
    venv_path = '/home/user/venv'
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} is missing."
    python_bin = os.path.join(venv_path, 'bin', 'python')
    assert os.path.isfile(python_bin), f"Python executable not found in {venv_path}/bin/."

def test_processed_data_exists_and_correct():
    path = '/home/user/processed_data.csv'
    assert os.path.isfile(path), f"Processed data file {path} is missing."

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 10, f"Expected 10 rows in processed_data.csv, found {len(rows)}."

    expected_columns = {'tx_id', 'user_id', 'amount', 'test_group', 'age_score'}
    assert set(reader.fieldnames) == expected_columns, f"Columns in processed_data.csv do not match expected. Found: {reader.fieldnames}"

    # Calculate median from original data to verify
    original_meta = '/home/user/user_metadata.csv'
    with open(original_meta, 'r', encoding='utf-8') as f:
        meta_reader = csv.DictReader(f)
        age_scores = [int(r['age_score']) for r in meta_reader if r['age_score'].strip()]

    age_scores.sort()
    n = len(age_scores)
    if n % 2 == 1:
        median = age_scores[n//2]
    else:
        median = (age_scores[n//2 - 1] + age_scores[n//2]) / 2.0
    median = int(median) # Should be 33

    # Check that missing users have the imputed median and age_score is integer
    for row in rows:
        age_str = row['age_score']
        assert '.' not in age_str, f"age_score {age_str} is not an integer string."
        age_val = int(age_str)
        if row['user_id'] in ['103', '107', '109']:
            assert age_val == median, f"User {row['user_id']} should have imputed age_score {median}, but got {age_val}."

def test_results_json_exists_and_format():
    path = '/home/user/results.json'
    assert os.path.isfile(path), f"Results file {path} is missing."

    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} does not contain valid JSON."

    expected_keys = {"imputed_median", "num_anomalies", "t_statistic", "p_value"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected. Found: {list(data.keys())}"

    assert isinstance(data['imputed_median'], int), "imputed_median must be an integer."
    assert data['imputed_median'] == 33, f"Expected imputed_median to be 33, got {data['imputed_median']}."

    assert isinstance(data['num_anomalies'], int), "num_anomalies must be an integer."
    assert isinstance(data['t_statistic'], (int, float)), "t_statistic must be a number."
    assert isinstance(data['p_value'], (int, float)), "p_value must be a number."

    # Check rounding to 4 decimal places
    t_stat_str = str(data['t_statistic'])
    p_val_str = str(data['p_value'])

    if '.' in t_stat_str:
        assert len(t_stat_str.split('.')[1]) <= 4, "t_statistic should be rounded to 4 decimal places."
    if '.' in p_val_str:
        assert len(p_val_str.split('.')[1]) <= 4, "p_value should be rounded to 4 decimal places."