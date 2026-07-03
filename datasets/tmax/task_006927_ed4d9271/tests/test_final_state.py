# test_final_state.py

import os
import json
import math
import pytest

def test_pipeline_script_exists():
    """Check if pipeline.py exists and configures OMP_NUM_THREADS."""
    script_path = '/home/user/pipeline.py'
    assert os.path.exists(script_path), f"{script_path} does not exist."
    with open(script_path, 'r') as f:
        content = f.read()
    assert 'OMP_NUM_THREADS' in content, "The script does not seem to configure OMP_NUM_THREADS."

def test_experiment_results():
    """Check if the experiment results match the expected ground truth."""
    results_path = '/home/user/experiment_results.json'
    assert os.path.exists(results_path), f"{results_path} does not exist."

    # Derive expected values using standard library
    # 1. Read and clean data
    raw_csv = '/home/user/raw_ratings.csv'
    assert os.path.exists(raw_csv), "raw_ratings.csv is missing."

    with open(raw_csv, 'r') as f:
        lines = f.read().strip().split('\n')

    header = lines[0].split(',')
    data = []
    for line in lines[1:]:
        parts = line.split(',')
        if len(parts) == 3 and parts[2].strip() != '':
            data.append((parts[0], parts[1], float(parts[2])))

    # Count ratings per user
    user_counts = {}
    for u, i, r in data:
        user_counts[u] = user_counts.get(u, 0) + 1

    valid_users = {u for u, c in user_counts.items() if c >= 3}

    # Pivot matrix
    all_items = sorted(list({i for u, i, r in data if u in valid_users}))
    valid_users_sorted = sorted(list(valid_users))

    matrix = []
    for u in valid_users_sorted:
        user_ratings = {i: r for u_id, i, r in data if u_id == u}
        row = [user_ratings.get(i, 0.0) for i in all_items]
        matrix.append(row)

    # KFold n_splits=3, shuffle=True, random_state=42
    # sklearn KFold random_state=42 with shuffle=True on 7 items produces specific folds
    # In scikit-learn, KFold uses numpy.random.RandomState(42).permutation(7)
    # The permutation of 7 elements with seed 42 is: [0, 1, 5, 4, 2, 6, 3]
    # Folds: 
    # Fold 0: test indices [0, 1, 5]
    # Fold 1: test indices [4, 2]
    # Fold 2: test indices [6, 3]

    indices = [0, 1, 5, 4, 2, 6, 3]
    folds = [
        (indices[3:], indices[0:3]),
        (indices[0:3] + indices[5:], indices[3:5]),
        (indices[0:5], indices[5:])
    ]

    def cosine_dist(v1, v2):
        dot = sum(x*y for x, y in zip(v1, v2))
        norm1 = math.sqrt(sum(x*x for x in v1))
        norm2 = math.sqrt(sum(y*y for y in v2))
        if norm1 == 0 or norm2 == 0:
            return 1.0
        return 1.0 - (dot / (norm1 * norm2))

    results = {}
    for k in [2, 3, 4]:
        fold_dists = []
        for train_idx, test_idx in folds:
            train_data = [matrix[i] for i in train_idx]
            test_data = [matrix[i] for i in test_idx]

            for test_vec in test_data:
                dists = [cosine_dist(test_vec, train_vec) for train_vec in train_data]
                dists.sort()
                k_nearest = dists[:k]
                fold_dists.append(sum(k_nearest) / len(k_nearest))

        results[k] = sum(fold_dists) / len(fold_dists)

    best_k = min(results, key=results.get)
    expected_best_mean_distance = round(results[best_k], 4)

    with open(results_path, 'r') as f:
        try:
            user_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not valid JSON.")

    assert 'best_k' in user_results, "Missing 'best_k' in results JSON."
    assert 'best_mean_distance' in user_results, "Missing 'best_mean_distance' in results JSON."

    assert user_results['best_k'] == best_k, f"Expected best_k to be {best_k}, got {user_results['best_k']}"
    assert user_results['best_mean_distance'] == expected_best_mean_distance, \
        f"Expected best_mean_distance to be {expected_best_mean_distance}, got {user_results['best_mean_distance']}"