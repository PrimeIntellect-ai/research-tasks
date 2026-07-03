# test_final_state.py
import os
import json
import csv
import math

def get_csv_data(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [[] for _ in header]
        for row in reader:
            for i, val in enumerate(row):
                data[i].append(float(val))
    return header, data

def mean(lst):
    return sum(lst) / len(lst)

def std(lst, m):
    # Population std dev to match pandas/numpy correlation logic (cov/sx*sy cancels out N or N-1 if consistent)
    # Actually pandas uses N-1, but for correlation coefficient the N-1 cancels out.
    return math.sqrt(sum((x - m)**2 for x in lst))

def calc_corr(xs, ys):
    mx = mean(xs)
    my = mean(ys)
    sx = std(xs, mx)
    sy = std(ys, my)
    if sx == 0 or sy == 0:
        return 0
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / (sx * sy)

def test_results_json_exists():
    assert os.path.exists("/home/user/results.json"), "/home/user/results.json does not exist."
    assert os.path.isfile("/home/user/results.json"), "/home/user/results.json is not a file."

def test_results_json_structure_and_values():
    with open("/home/user/results.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/results.json is not a valid JSON file."

    assert "dropped_features" in results, "Key 'dropped_features' missing from JSON."
    assert "significant_components" in results, "Key 'significant_components' missing from JSON."
    assert "model_accuracy" in results, "Key 'model_accuracy' missing from JSON."

    # Validate dropped_features by recomputing correlation
    header, data = get_csv_data("/home/user/chemical_data.csv")

    # Exclude target
    if "is_toxic" in header:
        target_idx = header.index("is_toxic")
        features = header[:target_idx] + header[target_idx+1:]
        feature_data = data[:target_idx] + data[target_idx+1:]
    else:
        features = header
        feature_data = data

    kept_cols = []
    dropped_cols = []
    kept_data = []

    for i, col in enumerate(features):
        col_data = feature_data[i]
        if not kept_cols:
            kept_cols.append(col)
            kept_data.append(col_data)
        else:
            max_corr = 0
            for k_data in kept_data:
                c = abs(calc_corr(col_data, k_data))
                if c > max_corr:
                    max_corr = c

            if max_corr > 0.85:
                dropped_cols.append(col)
            else:
                kept_cols.append(col)
                kept_data.append(col_data)

    assert isinstance(results["dropped_features"], list), "'dropped_features' must be a list."
    assert results["dropped_features"] == dropped_cols, f"Expected dropped_features to be {dropped_cols}, got {results['dropped_features']}."

    # Validate significant_components structure
    sig_comps = results["significant_components"]
    assert isinstance(sig_comps, list), "'significant_components' must be a list."
    assert all(isinstance(x, int) for x in sig_comps), "'significant_components' must contain only integers."
    assert all(0 <= x <= 4 for x in sig_comps), "'significant_components' values must be between 0 and 4."
    assert sig_comps == sorted(sig_comps), "'significant_components' must be sorted in ascending order."
    assert len(sig_comps) == len(set(sig_comps)), "'significant_components' must not contain duplicates."

    # Validate model_accuracy structure
    acc = results["model_accuracy"]
    assert isinstance(acc, float), "'model_accuracy' must be a float."
    assert 0.0 <= acc <= 1.0, "'model_accuracy' must be between 0.0 and 1.0."

    # Check if rounded to 4 decimal places
    acc_str = str(acc)
    if "." in acc_str:
        decimals = len(acc_str.split(".")[1])
        assert decimals <= 4, "'model_accuracy' should be rounded to exactly 4 decimal places."