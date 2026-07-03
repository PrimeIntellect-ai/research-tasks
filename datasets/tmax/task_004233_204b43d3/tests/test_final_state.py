# test_final_state.py

import os
import csv
import math

def test_rust_project_exists():
    project_dir = '/home/user/ml_pipeline'
    cargo_toml = os.path.join(project_dir, 'Cargo.toml')

    assert os.path.isdir(project_dir), f"Rust project directory not found: {project_dir}"
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found: {cargo_toml}"

def test_train_processed_csv():
    train_file = '/home/user/train_processed.csv'
    assert os.path.isfile(train_file), f"Processed train file not found: {train_file}"

    with open(train_file, 'r', newline='') as f:
        reader = list(csv.DictReader(f))

        assert f.name.endswith('train_processed.csv')

        # Check header
        assert reader[0].keys() == {'id', 'feature_x', 'label'}, "Header is incorrect in train_processed.csv"

        # Check total rows
        assert len(reader) == 80, f"Expected 80 data rows in train_processed.csv, got {len(reader)}"

        # Check imputation
        # id 8 was missing, should be 10.0
        row_8 = next((r for r in reader if r['id'] == '8'), None)
        assert row_8 is not None, "Row with id 8 missing in train_processed.csv"

        try:
            val_8 = float(row_8['feature_x'])
        except ValueError:
            assert False, f"feature_x for id 8 is not a valid float: {row_8['feature_x']}"

        assert math.isclose(val_8, 10.0), f"Data leak detected or incorrect imputation in train set. Expected 10.0, got {val_8}"

        # id 1 was not missing, should be 10.0
        row_1 = next((r for r in reader if r['id'] == '1'), None)
        assert row_1 is not None, "Row with id 1 missing in train_processed.csv"
        assert math.isclose(float(row_1['feature_x']), 10.0), "Original data was modified incorrectly"

def test_test_processed_csv():
    test_file = '/home/user/test_processed.csv'
    assert os.path.isfile(test_file), f"Processed test file not found: {test_file}"

    with open(test_file, 'r', newline='') as f:
        reader = list(csv.DictReader(f))

        # Check header
        assert reader[0].keys() == {'id', 'feature_x', 'label'}, "Header is incorrect in test_processed.csv"

        # Check total rows
        assert len(reader) == 20, f"Expected 20 data rows in test_processed.csv, got {len(reader)}"

        # Check imputation
        # id 84 was missing, should be 10.0
        row_84 = next((r for r in reader if r['id'] == '84'), None)
        assert row_84 is not None, "Row with id 84 missing in test_processed.csv"

        try:
            val_84 = float(row_84['feature_x'])
        except ValueError:
            assert False, f"feature_x for id 84 is not a valid float: {row_84['feature_x']}"

        assert math.isclose(val_84, 10.0), f"Data leak detected or incorrect imputation in test set. Expected 10.0, got {val_84}"

        # id 81 was not missing, should be 50.0
        row_81 = next((r for r in reader if r['id'] == '81'), None)
        assert row_81 is not None, "Row with id 81 missing in test_processed.csv"
        assert math.isclose(float(row_81['feature_x']), 50.0), "Original data was modified incorrectly"