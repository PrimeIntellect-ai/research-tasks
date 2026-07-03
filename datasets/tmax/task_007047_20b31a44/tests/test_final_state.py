# test_final_state.py

import os
import csv
import json
import math

def test_venv_exists():
    assert os.path.exists("/home/user/venv/bin/python"), "Virtual environment python binary not found."
    assert os.path.exists("/home/user/venv/bin/pytest"), "pytest not found in virtual environment."

def test_etl_script_exists():
    assert os.path.exists("/home/user/etl.py"), "etl.py script not found."

def test_transformed_metrics_csv():
    csv_path = "/home/user/transformed_metrics.csv"
    assert os.path.exists(csv_path), f"{csv_path} not found."

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        expected_fields = ["group", "count", "mean", "std", "ci_lower", "ci_upper"]
        assert fieldnames == expected_fields, f"Expected columns {expected_fields}, got {fieldnames}"

        rows = list(reader)
        assert len(rows) == 2, "Expected exactly 2 rows for 'control' and 'treatment'."

        data = {row['group']: row for row in rows}
        assert 'control' in data and 'treatment' in data, "Missing 'control' or 'treatment' group in CSV."

        # Check control values
        control = data['control']
        assert int(control['count']) == 500
        assert math.isclose(float(control['mean']), 149.6853, abs_tol=0.001)
        assert math.isclose(float(control['std']), 19.5593, abs_tol=0.001)
        assert math.isclose(float(control['ci_lower']), 147.9667, abs_tol=0.001)
        assert math.isclose(float(control['ci_upper']), 151.4038, abs_tol=0.001)

        # Check treatment values
        treatment = data['treatment']
        assert int(treatment['count']) == 500
        assert math.isclose(float(treatment['mean']), 145.4184, abs_tol=0.001)
        assert math.isclose(float(treatment['std']), 21.6508, abs_tol=0.001)
        assert math.isclose(float(treatment['ci_lower']), 143.5159, abs_tol=0.001)
        assert math.isclose(float(treatment['ci_upper']), 147.3208, abs_tol=0.001)

def test_ttest_results_json():
    json_path = "/home/user/ttest_results.json"
    assert os.path.exists(json_path), f"{json_path} not found."

    with open(json_path, 'r') as f:
        data = json.load(f)

    assert "t_stat" in data, "Missing 't_stat' in JSON."
    assert "p_value" in data, "Missing 'p_value' in JSON."

    assert math.isclose(data['t_stat'], 3.273, rel_tol=0.01), f"t_stat value {data['t_stat']} is incorrect."
    assert math.isclose(data['p_value'], 0.00109, rel_tol=0.01), f"p_value value {data['p_value']} is incorrect."

def test_test_etl_script_exists():
    assert os.path.exists("/home/user/test_etl.py"), "test_etl.py script not found."
    with open("/home/user/test_etl.py", 'r') as f:
        content = f.read()
        assert "test_numerical_accuracy" in content, "test_numerical_accuracy function not found in test_etl.py"

def test_pytest_output():
    log_path = "/home/user/pytest_output.txt"
    assert os.path.exists(log_path), f"{log_path} not found."

    with open(log_path, 'r') as f:
        content = f.read()
        assert "1 passed" in content, "pytest output does not show 1 passed test."