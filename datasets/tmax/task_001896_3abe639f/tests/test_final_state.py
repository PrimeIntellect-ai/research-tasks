# test_final_state.py
import os
import json
import math
import pytest

def load_data(filepath):
    X = []
    y = []
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            X.append([float(v) for v in parts[:-1]])
            y.append(int(float(parts[-1])))
    return X, y

def mean_std(X):
    n = len(X)
    n_features = len(X[0])
    means = [sum(X[i][j] for i in range(n)) / n for j in range(n_features)]
    stds = []
    for j in range(n_features):
        var = sum((X[i][j] - means[j]) ** 2 for i in range(n)) / n
        std = math.sqrt(var)
        stds.append(std if std != 0 else 1.0)
    return means, stds

def transform(X, means, stds):
    return [[(row[j] - means[j]) / stds[j] for j in range(len(row))] for row in X]

def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def knn_predict(X_train, y_train, X_test, k):
    preds = []
    for test_pt in X_test:
        dists = [(euclidean_distance(test_pt, train_pt), i) for i, train_pt in enumerate(X_train)]
        dists.sort()

        counts = {}
        for _, idx in dists[:k]:
            label = y_train[idx]
            counts[label] = counts.get(label, 0) + 1

        best_label = -1
        max_count = -1
        # To match sklearn, we resolve ties by taking the first encountered in sorted order
        # Actually sklearn picks the class with the lower class label or based on order,
        # but here the C++ code uses a map and iterates up to k.
        # Let's emulate the C++ map logic or just count.
        for _, idx in dists[:k]:
            label = y_train[idx]
            if counts[label] > max_count:
                max_count = counts[label]
                best_label = label
        preds.append(best_label)
    return preds

def compute_expected_results():
    X, y = load_data('/home/user/data/dataset.csv')
    n = len(X)
    folds = 5
    fold_size = n // folds

    best_k = 1
    best_acc = -1.0

    for k in [1, 3, 5, 7, 9]:
        total_acc = 0.0
        for i in range(folds):
            test_start = i * fold_size
            test_end = (i + 1) * fold_size

            X_test = X[test_start:test_end]
            y_test = y[test_start:test_end]
            X_train = X[:test_start] + X[test_end:]
            y_train = y[:test_start] + y[test_end:]

            means, stds = mean_std(X_train)
            X_train_scaled = transform(X_train, means, stds)
            X_test_scaled = transform(X_test, means, stds)

            preds = knn_predict(X_train_scaled, y_train, X_test_scaled, k)
            correct = sum(1 for p, true_y in zip(preds, y_test) if p == true_y)
            total_acc += correct / len(y_test)

        avg_acc = total_acc / folds
        if avg_acc > best_acc:
            best_acc = avg_acc
            best_k = k

    # Final evaluation
    means, stds = mean_std(X)
    X_scaled = transform(X, means, stds)

    new_point = [1.5, 2.0, -1.0, 0.5]
    new_point_scaled = transform([new_point], means, stds)[0]

    dists = [(euclidean_distance(new_point_scaled, pt), i) for i, pt in enumerate(X_scaled)]
    dists.sort()

    neighbors = [idx for _, idx in dists[:3]]

    counts = {}
    for _, idx in dists[:best_k]:
        label = y[idx]
        counts[label] = counts.get(label, 0) + 1

    best_label = -1
    max_count = -1
    for _, idx in dists[:best_k]:
        label = y[idx]
        if counts[label] > max_count:
            max_count = counts[label]
            best_label = label

    return best_k, best_acc, best_label, neighbors

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File {results_path} is missing."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    expected_k, expected_acc, expected_pred, expected_neighbors = compute_expected_results()

    assert "best_k" in results, "Missing 'best_k' in results."
    assert results["best_k"] == expected_k, f"Expected best_k={expected_k}, got {results['best_k']}"

    assert "best_cv_accuracy" in results, "Missing 'best_cv_accuracy' in results."
    assert abs(results["best_cv_accuracy"] - expected_acc) < 1e-4, f"Expected best_cv_accuracy ~ {expected_acc}, got {results['best_cv_accuracy']}"

    assert "new_point_prediction" in results, "Missing 'new_point_prediction' in results."
    assert results["new_point_prediction"] == expected_pred, f"Expected new_point_prediction={expected_pred}, got {results['new_point_prediction']}"

    assert "nearest_neighbor_indices" in results, "Missing 'nearest_neighbor_indices' in results."
    assert results["nearest_neighbor_indices"] == expected_neighbors, f"Expected nearest_neighbor_indices={expected_neighbors}, got {results['nearest_neighbor_indices']}"