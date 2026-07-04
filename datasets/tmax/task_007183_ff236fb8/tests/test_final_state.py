# test_final_state.py
import os
import csv
import pytest

def test_clean_data_content():
    expected_content = """id,value,label
1,10.0,0
2,10.2,0
3,10.1,0
4,10.1,0
5,10.3,0
6,15.5,1
7,10.1,0
8,10.2,0
9,10.2,0
10,10.4,0
11,20.0,1
12,10.1,0
13,10.0,0
14,9.9,0
15,14.0,1"""

    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.exists(clean_data_path), f"{clean_data_path} is missing."

    with open(clean_data_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {clean_data_path} does not match the expected forward-filled data."

def get_expected_f1(W, T, values, labels):
    tp = 0
    fp = 0
    fn = 0
    for i in range(W, len(values)):
        mean = sum(values[i-W:i]) / W
        pred = 1 if abs(values[i] - mean) > T else 0
        actual = labels[i]
        if pred == 1 and actual == 1:
            tp += 1
        elif pred == 1 and actual == 0:
            fp += 1
        elif pred == 0 and actual == 1:
            fn += 1
    if tp == 0:
        return 0.0
    return 2 * tp / (2 * tp + fp + fn)

def test_grid_results():
    grid_results_path = "/home/user/grid_results.csv"
    assert os.path.exists(grid_results_path), f"{grid_results_path} is missing."

    values = [10.0, 10.2, 10.1, 10.1, 10.3, 15.5, 10.1, 10.2, 10.2, 10.4, 20.0, 10.1, 10.0, 9.9, 14.0]
    labels = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]

    expected_results = {}
    for W in [2, 3, 4]:
        for T in [1.5, 2.0, 2.5]:
            f1 = get_expected_f1(W, T, values, labels)
            expected_results[(W, T)] = f"{f1:.4f}"

    with open(grid_results_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["W", "T", "F1"], f"Header in {grid_results_path} must be exactly W,T,F1."

        actual_results = {}
        for row in reader:
            assert len(row) == 3, f"Invalid row format in {grid_results_path}: {row}"
            w, t, f1 = row
            actual_results[(int(w), float(t))] = f1

    assert len(actual_results) == 9, f"Expected 9 result rows, found {len(actual_results)}."

    for w_t, expected_f1 in expected_results.items():
        assert w_t in actual_results, f"Missing result for W={w_t[0]}, T={w_t[1]}."
        actual_f1 = actual_results[w_t]
        assert actual_f1 == expected_f1, f"F1 mismatch for W={w_t[0]}, T={w_t[1]}: expected {expected_f1}, got {actual_f1}."