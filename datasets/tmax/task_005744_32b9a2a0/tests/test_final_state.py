# test_final_state.py

import os
import pytest

def test_knn_imputation_results():
    dataset_path = "/home/user/dataset.txt"
    assert os.path.exists(dataset_path), f"Dataset file {dataset_path} is missing."

    complete_rows = []
    missing_rows = []

    with open(dataset_path, "r") as f:
        lines = f.read().strip().split('\n')
        for line in lines[1:]:  # Skip header
            parts = line.strip().split()
            if not parts:
                continue
            id_val = int(parts[0])
            x1 = int(parts[1])
            x2 = int(parts[2])
            if parts[3] == '?':
                missing_rows.append((id_val, x1, x2))
            else:
                complete_rows.append((id_val, x1, x2, float(parts[3])))

    # 1. Recompute LOOCV to find optimal K
    mses = {1: 0.0, 2: 0.0, 3: 0.0}
    for i, row in enumerate(complete_rows):
        id_val, x1, x2, y = row
        distances = []
        for j, other in enumerate(complete_rows):
            if i == j:
                continue
            o_id, o_x1, o_x2, o_y = other
            # Manhattan distance
            dist = abs(x1 - o_x1) + abs(x2 - o_x2)
            distances.append((dist, o_id, o_y))

        # Sort by distance, then by ID to break ties
        distances.sort(key=lambda x: (x[0], x[1]))

        for k in [1, 2, 3]:
            pred = sum(d[2] for d in distances[:k]) / k
            mses[k] += (pred - y) ** 2

    # Optimal K minimizes MSE, tie-breaks with smaller K
    optimal_k = min([1, 2, 3], key=lambda k: (mses[k], k))

    # 2. Recompute expected imputed values
    expected_imputed = []
    for row in missing_rows:
        id_val, x1, x2 = row
        distances = []
        for other in complete_rows:
            o_id, o_x1, o_x2, o_y = other
            dist = abs(x1 - o_x1) + abs(x2 - o_x2)
            distances.append((dist, o_id, o_y))

        distances.sort(key=lambda x: (x[0], x[1]))
        pred = sum(d[2] for d in distances[:optimal_k]) / optimal_k
        expected_imputed.append((id_val, round(pred, 2)))

    expected_imputed.sort(key=lambda x: x[0])

    # 3. Validate optimal_k.txt
    k_path = "/home/user/optimal_k.txt"
    assert os.path.exists(k_path), f"File {k_path} was not created."
    with open(k_path, "r") as f:
        k_val = f.read().strip()
    assert k_val == str(optimal_k), f"Expected optimal K to be {optimal_k}, but got '{k_val}'."

    # 4. Validate imputed.txt
    imputed_path = "/home/user/imputed.txt"
    assert os.path.exists(imputed_path), f"File {imputed_path} was not created."

    actual_imputed = []
    with open(imputed_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            assert len(parts) == 2, f"Invalid format in {imputed_path}: '{line.strip()}'"
            actual_imputed.append((int(parts[0]), float(parts[1])))

    assert len(actual_imputed) == len(expected_imputed), (
        f"Expected {len(expected_imputed)} imputed values, but found {len(actual_imputed)}."
    )

    for act, exp in zip(actual_imputed, expected_imputed):
        assert act[0] == exp[0], f"Expected ID {exp[0]} in order, got {act[0]}."
        # Check formatting exactly 2 decimal places (string comparison)
        expected_str = f"{exp[1]:.2f}"
        actual_str = f"{act[1]:.2f}"
        assert actual_str == expected_str, (
            f"For ID {exp[0]}, expected imputed value {expected_str}, but got {actual_str}."
        )