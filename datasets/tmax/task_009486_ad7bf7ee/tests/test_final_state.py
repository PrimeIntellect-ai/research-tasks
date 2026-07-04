# test_final_state.py
import os
import csv
import re

def test_features_csv_exists():
    assert os.path.isfile("/home/user/mlops_pipeline/artifacts/features.csv"), "features.csv was not generated."

def test_author_id_imputation_and_type():
    csv_path = "/home/user/mlops_pipeline/artifacts/features.csv"
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 7, "Expected 7 rows in features.csv."

    expected_author_ids = ['10', '-1', '20', '-1', '30', '-1', '40']
    actual_author_ids = [row['author_id'] for row in rows]

    for i, (actual, expected) in enumerate(zip(actual_author_ids, expected_author_ids)):
        assert actual == expected, f"Row {i+1}: expected author_id '{expected}', got '{actual}'. Ensure missing values are imputed with -1 and the column is cast to integer."

def test_svd_columns_exist():
    csv_path = "/home/user/mlops_pipeline/artifacts/features.csv"
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

    assert "svd_0" in fieldnames, "Column 'svd_0' is missing from features.csv."
    assert "svd_1" in fieldnames, "Column 'svd_1' is missing from features.csv."

    # Check that they are floats
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            try:
                float(row["svd_0"])
                float(row["svd_1"])
            except ValueError:
                assert False, f"Row {i+1}: svd_0 and svd_1 must be valid floats."

def test_build_features_script_fixed():
    script_path = "/home/user/mlops_pipeline/build_features.py"
    with open(script_path, "r") as f:
        content = f.read()

    # Check for random_state=42
    assert re.search(r"random_state\s*=\s*42", content), "TruncatedSVD is not initialized with random_state=42 in build_features.py."

    # Check for imputation logic
    assert "-1" in content, "Missing value imputation with -1 not found in build_features.py."
    assert "int" in content.lower(), "Integer casting logic not found in build_features.py."