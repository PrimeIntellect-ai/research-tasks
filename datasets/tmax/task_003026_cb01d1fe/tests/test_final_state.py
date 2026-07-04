# test_final_state.py

import os
import json
import math
import pytest

def test_results_json_exists_and_correct():
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"Expected output file {results_path} does not exist. Did the script run successfully?"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert 't_stat' in results, f"Key 't_stat' missing in {results_path}"
    assert 'p_value' in results, f"Key 'p_value' missing in {results_path}"

    expected_t = -7.067332308696338
    expected_p = 0.00010915609460298918

    t_stat = results['t_stat']
    p_value = results['p_value']

    assert isinstance(t_stat, (int, float)), "t_stat must be a float"
    assert isinstance(p_value, (int, float)), "p_value must be a float"

    assert math.isclose(t_stat, expected_t, rel_tol=1e-3), f"t_stat {t_stat} does not match expected value {expected_t}. Was the invalid data dropped correctly?"
    assert math.isclose(p_value, expected_p, rel_tol=1e-3), f"p_value {p_value} does not match expected value {expected_p}. Was the invalid data dropped correctly?"

def test_report_png_exists():
    report_path = '/home/user/report.png'
    assert os.path.isfile(report_path), f"Expected plot file {report_path} does not exist. Did the script crash due to the matplotlib backend?"
    assert os.path.getsize(report_path) > 0, f"Plot file {report_path} is empty."