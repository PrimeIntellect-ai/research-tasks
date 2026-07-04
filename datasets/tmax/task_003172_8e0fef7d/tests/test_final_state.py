# test_final_state.py

import os
import json
import csv
import math

def test_results_json():
    result_path = "/home/user/results.json"
    assert os.path.isfile(result_path), f"File {result_path} is missing."

    # Recompute ground truth using standard library
    data_a_path = "/home/user/data_a.csv"
    data_b_path = "/home/user/data_b.csv"

    with open(data_a_path, 'r') as f:
        reader = csv.DictReader(f)
        data_a = {row['id']: row for row in reader}

    with open(data_b_path, 'r') as f:
        reader = csv.DictReader(f)
        data_b = {row['id']: row for row in reader}

    # Join and Clean
    merged = []
    for id_val, row_a in data_a.items():
        if id_val in data_b:
            row_b = data_b[id_val]
            merged_row = {**row_a, **row_b}
            # Check for NA or empty
            if any(v == "NA" or v == "" for v in merged_row.values()):
                continue
            merged_row['id'] = int(merged_row['id'])
            for k in ['f1', 'f2', 'f3', 'f4', 'y']:
                merged_row[k] = float(merged_row[k])
            merged.append(merged_row)

    # Sort and Split
    merged.sort(key=lambda x: x['id'])
    train_size = (len(merged) * 80) // 100
    train = merged[:train_size]
    test = merged[train_size:]

    # Correlation on Train
    def mean(vals):
        return sum(vals) / len(vals)

    def corr(xs, ys):
        mx = mean(xs)
        my = mean(ys)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        var_x = sum((x - mx) ** 2 for x in xs)
        var_y = sum((y - my) ** 2 for y in ys)
        if var_x == 0 or var_y == 0:
            return 0
        return cov / math.sqrt(var_x * var_y)

    y_train = [row['y'] for row in train]
    features = ['f1', 'f2', 'f3', 'f4']
    corrs = {}
    for f in features:
        xs = [row[f] for row in train]
        corrs[f] = corr(xs, y_train)

    best_feature = max(corrs, key=lambda k: abs(corrs[k]))

    # Linear Regression on Train
    x_train = [row[best_feature] for row in train]
    mx = mean(x_train)
    my = mean(y_train)
    cov = sum((x - mx) * (y - my) for x, y in zip(x_train, y_train))
    var_x = sum((x - mx) ** 2 for x in x_train)

    slope = cov / var_x
    intercept = my - slope * mx

    # Evaluate on Test
    x_test = [row[best_feature] for row in test]
    y_test = [row['y'] for row in test]
    preds = [slope * x + intercept for x in x_test]
    mse = mean([(y - p) ** 2 for y, p in zip(y_test, preds)])

    expected = {
        "selected_feature": best_feature,
        "slope": round(slope, 4),
        "intercept": round(intercept, 4),
        "test_mse": round(mse, 4)
    }

    # Load actual results
    with open(result_path, 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{result_path} is not valid JSON."

    assert "selected_feature" in actual, "Key 'selected_feature' missing in results.json"
    assert "slope" in actual, "Key 'slope' missing in results.json"
    assert "intercept" in actual, "Key 'intercept' missing in results.json"
    assert "test_mse" in actual, "Key 'test_mse' missing in results.json"

    assert actual["selected_feature"] == expected["selected_feature"], f"Expected feature {expected['selected_feature']}, got {actual['selected_feature']}"
    assert math.isclose(actual["slope"], expected["slope"], abs_tol=1e-3), f"Expected slope {expected['slope']}, got {actual['slope']}"
    assert math.isclose(actual["intercept"], expected["intercept"], abs_tol=1e-3), f"Expected intercept {expected['intercept']}, got {actual['intercept']}"
    assert math.isclose(actual["test_mse"], expected["test_mse"], abs_tol=1e-3), f"Expected test_mse {expected['test_mse']}, got {actual['test_mse']}"

def test_go_module_exists():
    go_mod_path = "/home/user/go.mod"
    assert os.path.isfile(go_mod_path), "Go module was not initialized (go.mod is missing)."
    with open(go_mod_path, "r") as f:
        content = f.read()
    assert "module ml_task" in content, "Go module name is not 'ml_task'."