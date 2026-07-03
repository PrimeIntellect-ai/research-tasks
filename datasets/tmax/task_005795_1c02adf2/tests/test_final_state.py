# test_final_state.py
import os
import csv
import math

def test_predictions_file_exists():
    assert os.path.isfile("/home/user/fixed_predictions.csv"), "/home/user/fixed_predictions.csv is missing. Did you compile, run, and rename the output file?"

def test_predictions_content():
    # Recompute the expected values based on the training set (first 6 rows)
    train_features = [2.0, 2.5, 3.0, 8.0, 8.5, 9.0]
    test_features = [(6, 2.2), (7, 8.8), (8, 5.0), (9, 5.6)]

    # Expected ETL statistics
    mean = sum(train_features) / len(train_features)
    variance = sum((x - mean) ** 2 for x in train_features) / len(train_features)
    stddev = math.sqrt(variance)

    # Calculate expected z-scores for test set
    expected_z_scores = {id_: (feat - mean) / stddev for id_, feat in test_features}

    # Calculate expected Naive Bayes parameters
    train_z_scores = [(x - mean) / stddev for x in train_features]
    z_0 = train_z_scores[:3] # Labels are 0 for first 3
    z_1 = train_z_scores[3:] # Labels are 1 for next 3

    mu_0 = sum(z_0) / len(z_0)
    var_0 = sum((x - mu_0) ** 2 for x in z_0) / len(z_0)

    mu_1 = sum(z_1) / len(z_1)
    var_1 = sum((x - mu_1) ** 2 for x in z_1) / len(z_1)

    # Calculate expected predictions
    expected_preds = {}
    for id_, z in expected_z_scores.items():
        p0 = math.exp(-((z - mu_0) ** 2) / (2 * var_0)) / math.sqrt(2 * math.pi * var_0)
        p1 = math.exp(-((z - mu_1) ** 2) / (2 * var_1)) / math.sqrt(2 * math.pi * var_1)
        expected_preds[id_] = 1 if p1 > p0 else 0

    with open("/home/user/fixed_predictions.csv", "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 4, f"Expected 4 rows in predictions.csv, got {len(rows)}"

    for row in rows:
        id_ = int(row["id"])
        z_score = float(row["z_score"])
        pred = int(row["predicted_label"])

        assert id_ in expected_z_scores, f"Unexpected id {id_} in predictions"

        expected_z = expected_z_scores[id_]
        assert math.isclose(z_score, expected_z, abs_tol=1e-5), f"For id {id_}, expected z_score ~{expected_z:.6f}, got {z_score}. The ETL data leakage bug might not be fully fixed."

        expected_pred = expected_preds[id_]
        assert pred == expected_pred, f"For id {id_}, expected predicted_label {expected_pred}, got {pred}."

def test_c_code_modifications():
    assert os.path.isfile("/home/user/pipeline.c"), "/home/user/pipeline.c is missing"
    with open("/home/user/pipeline.c", "r") as f:
        content = f.read()

    # The normalisation loop should still use TOTAL_SIZE
    assert "data[i].z_score = (data[i].feature - mean) / stddev;" in content, "The normalization assignment was unexpectedly altered."