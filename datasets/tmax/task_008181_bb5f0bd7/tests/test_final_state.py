# test_final_state.py
import os
import csv
import math

def test_scripts_exist_and_executable():
    scripts = [
        '/home/user/clean.py',
        '/home/user/recommend.py',
        '/home/user/evaluate.sh'
    ]
    for script in scripts:
        assert os.path.exists(script), f"Script {script} is missing."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_clean_features_csv():
    filepath = '/home/user/clean_features.csv'
    assert os.path.exists(filepath), f"{filepath} is missing."

    expected_data = {
        'A': [1.0, -10.0, 0.1],
        'B': [2.0, 1.0, 0.2],
        'C': [10.0, 1.5, 0.3],
        'D': [10.0, 2.0, 0.4],
        'E': [1.5, -10.0, 0.5],
    }

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'f1', 'f2', 'f3'], f"Incorrect header in {filepath}."

        parsed_data = {}
        for row in reader:
            assert len(row) == 4, f"Row {row} does not have 4 columns."
            parsed_data[row[0]] = [float(x) for x in row[1:]]

            # Check formatting (4 decimal places)
            for val in row[1:]:
                assert len(val.split('.')[-1]) == 4, f"Value {val} is not formatted to 4 decimal places."

    assert set(parsed_data.keys()) == set(expected_data.keys()), "Missing or extra IDs in cleaned features."

    for k, v in expected_data.items():
        for expected_val, actual_val in zip(v, parsed_data[k]):
            assert math.isclose(expected_val, actual_val, rel_tol=1e-5), f"Incorrect cleaned value for {k}: expected {expected_val}, got {actual_val}."

def test_nn_results_csv():
    filepath = '/home/user/nn_results.csv'
    assert os.path.exists(filepath), f"{filepath} is missing."

    expected_nn = {
        'A': ['E', 'B'],
        'B': ['C', 'D'],
        'C': ['D', 'B'],
        'D': ['C', 'B'],
        'E': ['A', 'B'],
    }

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'nn1_id', 'nn2_id'], f"Incorrect header in {filepath}."

        parsed_nn = {}
        for row in reader:
            assert len(row) == 3, f"Row {row} does not have 3 columns."
            parsed_nn[row[0]] = [row[1], row[2]]

    assert parsed_nn == expected_nn, f"Incorrect nearest neighbors. Expected {expected_nn}, got {parsed_nn}."

def test_accuracy_txt():
    filepath = '/home/user/accuracy.txt'
    assert os.path.exists(filepath), f"{filepath} is missing."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "0.20", f"Incorrect accuracy in {filepath}. Expected '0.20', got '{content}'."