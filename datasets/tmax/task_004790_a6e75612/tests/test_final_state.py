# test_final_state.py

import os
import json
import math
import pytest

def test_most_similar_exp_output():
    output_path = "/home/user/most_similar_exp.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Recompute the expected result based on the current JSON files in the directory
    experiments_dir = "/home/user/experiments"
    target_path = os.path.join(experiments_dir, "exp_target.json")

    assert os.path.isfile(target_path), f"Target experiment file {target_path} is missing."

    with open(target_path, 'r') as f:
        target_data = json.load(f)

    def get_features(data):
        f1 = data.get("learning_rate", 0.0) * 1000.0
        f2 = data.get("batch_size", 0) / 64.0
        f3 = (data.get("accuracy", 0.0) - 0.5) * 10.0
        return f1, f2, f3

    target_features = get_features(target_data)

    closest_id = None
    min_dist_sq = float('inf')

    for filename in os.listdir(experiments_dir):
        if not filename.endswith(".json"):
            continue
        if filename == "exp_target.json":
            continue

        file_path = os.path.join(experiments_dir, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)

        features = get_features(data)

        dist_sq = sum((t - f) ** 2 for t, f in zip(target_features, features))

        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest_id = data.get("id")

    # Read the actual output
    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == closest_id, f"Expected '{closest_id}', but got '{actual_output}' in {output_path}."