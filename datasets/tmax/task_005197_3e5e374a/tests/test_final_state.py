# test_final_state.py
import os
import csv
import json
import math

def test_cleaned_reviews_csv():
    cleaned_path = "/home/user/cleaned_reviews.csv"
    original_path = "/home/user/reviews.csv"

    assert os.path.isfile(cleaned_path), f"Missing file: {cleaned_path}"
    assert os.path.isfile(original_path), f"Missing file: {original_path}"

    # Read original to get valid rows
    original_valid = {}
    with open(original_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row["text"]:
                continue
            try:
                rating = float(row["rating"])
                if 1.0 <= rating <= 5.0:
                    original_valid[row["id"]] = rating
            except ValueError:
                pass

    with open(cleaned_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["id", "text", "final_rating"], \
            f"Incorrect columns in {cleaned_path}. Expected ['id', 'text', 'final_rating']"

        previous_id = -1
        for row in reader:
            current_id = int(row["id"])
            assert current_id > previous_id, "Rows are not sorted by 'id' in ascending order."
            previous_id = current_id

            assert row["text"].strip() != "", f"Row with id {current_id} has missing text."

            final_rating = float(row["final_rating"])
            assert 1.0 <= final_rating <= 5.0, \
                f"final_rating {final_rating} for id {current_id} is out of bounds [1.0, 5.0]."

            if row["id"] in original_valid:
                expected_rating = original_valid[row["id"]]
                assert math.isclose(final_rating, expected_rating, rel_tol=1e-5), \
                    f"Valid rating changed for id {current_id}. Expected {expected_rating}, got {final_rating}."

def test_metrics_json():
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), f"Missing file: {metrics_path}"

    with open(metrics_path, "r", encoding="utf-8") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} is not a valid JSON file."

    expected_keys = {"t_test_p_value", "train_mse", "imputed_mean"}
    assert set(metrics.keys()) == expected_keys, \
        f"Incorrect keys in metrics.json. Expected {expected_keys}, got {set(metrics.keys())}."

    p_val = metrics["t_test_p_value"]
    mse = metrics["train_mse"]
    imp_mean = metrics["imputed_mean"]

    assert isinstance(p_val, (int, float)), "t_test_p_value must be a float."
    assert 0.0 <= p_val <= 1.0, f"t_test_p_value {p_val} is out of bounds [0, 1]."

    assert isinstance(mse, (int, float)), "train_mse must be a float."
    assert mse >= 0.0, f"train_mse {mse} cannot be negative."

    assert isinstance(imp_mean, (int, float)), "imputed_mean must be a float."
    assert 1.0 <= imp_mean <= 5.0, f"imputed_mean {imp_mean} is out of bounds [1.0, 5.0]."