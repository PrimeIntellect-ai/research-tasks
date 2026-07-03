# test_final_state.py

import os
import json
import sqlite3
import csv
import math
import pytest

RAW_DATA_PATH = '/home/user/raw_data.csv'
DB_PATH = '/home/user/cleaned_data.db'
RESULTS_PATH = '/home/user/results.json'

def compute_expected_stats():
    if not os.path.exists(RAW_DATA_PATH):
        return None

    with open(RAW_DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    cleaned = []
    for row in data:
        if row['sensor_a'] == '' or row['sensor_b'] == '' or row['sensor_a'] == 'nan' or row['sensor_b'] == 'nan':
            continue
        cleaned.append(row)

    value_c_valid = sorted([float(r['value_c']) for r in cleaned if r['value_c'] not in ('', 'nan')])
    n_c = len(value_c_valid)
    if n_c % 2 == 1:
        median_c = value_c_valid[n_c // 2]
    else:
        median_c = (value_c_valid[n_c // 2 - 1] + value_c_valid[n_c // 2]) / 2.0

    for r in cleaned:
        if r['value_c'] in ('', 'nan'):
            r['value_c'] = median_c
        else:
            r['value_c'] = float(r['value_c'])
        r['sensor_a'] = float(r['sensor_a'])
        r['sensor_b'] = float(r['sensor_b'])

    mean_a = sum(r['sensor_a'] for r in cleaned) / len(cleaned)
    mean_b = sum(r['sensor_b'] for r in cleaned) / len(cleaned)

    cov_ab = sum((r['sensor_a'] - mean_a) * (r['sensor_b'] - mean_b) for r in cleaned)
    var_a = sum((r['sensor_a'] - mean_a)**2 for r in cleaned)
    var_b = sum((r['sensor_b'] - mean_b)**2 for r in cleaned)

    corr = cov_ab / math.sqrt(var_a * var_b)

    treatment = [r['value_c'] for r in cleaned if r['group'] == 'treatment']
    control = [r['value_c'] for r in cleaned if r['group'] == 'control']

    mean_t = sum(treatment) / len(treatment)
    mean_c = sum(control) / len(control)

    var_t = sum((x - mean_t)**2 for x in treatment) / (len(treatment) - 1)
    var_c = sum((x - mean_c)**2 for x in control) / (len(control) - 1)

    t_stat = (mean_t - mean_c) / math.sqrt(var_t / len(treatment) + var_c / len(control))

    return {
        'count': len(cleaned),
        'correlation': round(corr, 4),
        't_statistic': round(t_stat, 4)
    }

def test_cleaned_data_db():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} was not created."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensor_data';")
        table_exists = cursor.fetchone()
        assert table_exists is not None, "Table 'sensor_data' does not exist in the database."

        cursor.execute("SELECT COUNT(*) FROM sensor_data;")
        count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sensor_data WHERE value_c IS NULL OR value_c = 'nan' OR value_c = '';")
        null_c_count = cursor.fetchone()[0]

        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"SQLite error: {e}")

    expected = compute_expected_stats()
    if expected:
        assert count == expected['count'], f"Expected {expected['count']} rows in sensor_data, but found {count}."

    assert null_c_count == 0, "There are still null/missing values in the value_c column."

def test_results_json():
    assert os.path.exists(RESULTS_PATH), f"Results file {RESULTS_PATH} was not created."

    with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} does not contain valid JSON.")

    expected_keys = {"correlation", "t_statistic", "p_value"}
    assert set(results.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}. Found: {list(results.keys())}"

    expected = compute_expected_stats()
    if expected:
        assert math.isclose(results['correlation'], expected['correlation'], abs_tol=0.001), \
            f"Expected correlation ~{expected['correlation']}, got {results['correlation']}"
        assert math.isclose(results['t_statistic'], expected['t_statistic'], abs_tol=0.001), \
            f"Expected t_statistic ~{expected['t_statistic']}, got {results['t_statistic']}"

        # p-value for this specific test case should be very close to 0
        assert isinstance(results['p_value'], (int, float)), "p_value must be a number"
        assert 0.0 <= results['p_value'] <= 1.0, "p_value must be between 0 and 1"