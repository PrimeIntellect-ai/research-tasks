import os
import csv
import math

def test_final_state():
    dataset_path = "/home/user/dataset.csv"
    train_clean_path = "/home/user/train_clean.csv"
    test_clean_path = "/home/user/test_clean.csv"

    assert os.path.isfile(dataset_path), f"Missing dataset file: {dataset_path}"
    assert os.path.isfile(train_clean_path), f"Missing train output file: {train_clean_path}"
    assert os.path.isfile(test_clean_path), f"Missing test output file: {test_clean_path}"

    # Read the original dataset
    original_data = []
    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            original_data.append({
                "id": int(row["id"]),
                "category": row["category"],
                "measurement": float(row["measurement"])
            })

    # Assert correct row counts
    assert len(original_data) == 1000, "Original dataset should have 1000 rows"

    # Compute Train statistics
    train_data = original_data[:800]
    test_data = original_data[800:]

    valid_train_measurements = [row["measurement"] for row in train_data if row["measurement"] != -999.0]

    train_mean = sum(valid_train_measurements) / len(valid_train_measurements)
    train_variance = sum((x - train_mean) ** 2 for x in valid_train_measurements) / len(valid_train_measurements)
    train_std = math.sqrt(train_variance)

    # Read test output
    test_clean = []
    with open(test_clean_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_clean.append({
                "id": int(row["id"]),
                "category": row["category"],
                "measurement": float(row["measurement"])
            })

    assert len(test_clean) == 200, f"Expected 200 rows in test_clean.csv, got {len(test_clean)}"

    # Validate test set values
    for orig, clean in zip(test_data, test_clean):
        assert orig["id"] == clean["id"], "ID mismatch in test output"
        assert orig["category"] == clean["category"], "Category mismatch in test output"

        val = orig["measurement"]
        if val == -999.0:
            val = train_mean

        expected_norm = (val - train_mean) / train_std
        expected_norm_rounded = round(expected_norm, 4)

        # Allow small floating point differences due to C++ formatting
        assert abs(clean["measurement"] - expected_norm_rounded) <= 0.0001, \
            f"Row ID {orig['id']}: expected normalized value ~{expected_norm_rounded}, got {clean['measurement']}"

    # Read train output
    train_clean = []
    with open(train_clean_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            train_clean.append({
                "id": int(row["id"]),
                "category": row["category"],
                "measurement": float(row["measurement"])
            })

    assert len(train_clean) == 800, f"Expected 800 rows in train_clean.csv, got {len(train_clean)}"

    # Validate train set values
    for orig, clean in zip(train_data, train_clean):
        assert orig["id"] == clean["id"], "ID mismatch in train output"
        assert orig["category"] == clean["category"], "Category mismatch in train output"

        val = orig["measurement"]
        if val == -999.0:
            val = train_mean

        expected_norm = (val - train_mean) / train_std
        expected_norm_rounded = round(expected_norm, 4)

        assert abs(clean["measurement"] - expected_norm_rounded) <= 0.0001, \
            f"Row ID {orig['id']}: expected normalized value ~{expected_norm_rounded}, got {clean['measurement']}"