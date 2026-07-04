# test_final_state.py
import os
import json
import csv

def test_metrics_json():
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"{metrics_path} does not exist."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} is not a valid JSON file."

    assert "train_avg_sim" in metrics, "metrics.json is missing the 'train_avg_sim' key."
    assert "test_avg_sim" in metrics, "metrics.json is missing the 'test_avg_sim' key."
    assert isinstance(metrics["train_avg_sim"], (int, float)), "'train_avg_sim' must be a number."
    assert isinstance(metrics["test_avg_sim"], (int, float)), "'test_avg_sim' must be a number."

def test_recommendations_csv():
    recs_path = '/home/user/recommendations.csv'
    assert os.path.isfile(recs_path), f"{recs_path} does not exist."

    with open(recs_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "title", "similarity"], "CSV columns must be exactly: id, title, similarity"

        rows = list(reader)
        assert len(rows) == 2, f"Expected exactly 2 recommendations, but found {len(rows)}."

        try:
            id_0 = int(rows[0][0])
            sim_0 = float(rows[0][2])
            sim_1 = float(rows[1][2])
        except ValueError:
            assert False, "CSV contains invalid data types for 'id' or 'similarity'."

        assert id_0 == 2, f"The top recommendation should be id 2, but got {id_0}."
        assert sim_0 >= sim_1, "Recommendations must be sorted by similarity in descending order."