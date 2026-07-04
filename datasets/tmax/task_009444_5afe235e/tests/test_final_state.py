# test_final_state.py

import os
import math
import pytest

def sgn(z):
    if z > 0: return 1
    if z < 0: return -1
    return 0

def compute_expected_data():
    mesh_x = []
    mesh_T = []
    for i in range(101):
        z = (i - 50) / 50.0
        x = 5.0 + 5.0 * sgn(z) * (z ** 2)
        T = 40.0 + 50.0 * math.exp(-0.5 * (x - 5.0)**2)
        mesh_x.append(x)
        mesh_T.append(T)

    primers_path = '/home/user/primers.txt'
    if not os.path.exists(primers_path):
        return [], 0, 0, 0

    with open(primers_path, 'r') as f:
        primers = [line.strip() for line in f if line.strip()]

    expected_data = []
    for seq in primers:
        gc_count = seq.count('G') + seq.count('C')
        f_gc = gc_count / len(seq)
        Tm = 50.0 + 40.0 * f_gc

        best_i = 0
        min_diff = float('inf')
        for i in range(101):
            diff = abs(mesh_T[i] - Tm)
            if diff < min_diff - 1e-9:
                min_diff = diff
                best_i = i

        expected_data.append({
            'Sequence': seq,
            'f_GC': f_gc,
            'Tm': Tm,
            'Optimal_X': mesh_x[best_i]
        })

    if not expected_data:
        return expected_data, 0, 0, 0

    x_vals = [d['f_GC'] for d in expected_data]
    y_vals = [d['Optimal_X'] for d in expected_data]
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n

    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    den = sum((x - mean_x)**2 for x in x_vals)
    slope = num / den if den != 0 else 0
    intercept = mean_y - slope * mean_x

    rss = sum((y - (slope * x + intercept))**2 for x, y in zip(x_vals, y_vals))

    return expected_data, slope, intercept, rss

def test_training_data_csv():
    csv_path = '/home/user/training_data.csv'
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."

    expected_data, _, _, _ = compute_expected_data()
    assert expected_data, "Could not compute expected data, missing primers.txt?"

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_data) + 1, "CSV row count mismatch."
    assert lines[0] == "Sequence,f_GC,Tm,Optimal_X", "CSV header mismatch."

    for i, expected in enumerate(expected_data):
        parts = lines[i+1].split(',')
        assert len(parts) == 4, f"Row {i+1} does not have 4 columns."
        assert parts[0] == expected['Sequence'], f"Row {i+1} Sequence mismatch."
        assert abs(float(parts[1]) - expected['f_GC']) < 1e-3, f"Row {i+1} f_GC mismatch."
        assert abs(float(parts[2]) - expected['Tm']) < 1e-3, f"Row {i+1} Tm mismatch."
        assert abs(float(parts[3]) - expected['Optimal_X']) < 1e-3, f"Row {i+1} Optimal_X mismatch."

def test_stats_log():
    log_path = '/home/user/stats.log'
    assert os.path.exists(log_path), f"Expected output file {log_path} does not exist."

    _, exp_slope, exp_intercept, exp_rss = compute_expected_data()

    with open(log_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 3, "stats.log must contain exactly 3 comma-separated values."

    act_slope, act_intercept, act_rss = map(float, parts)

    assert abs(act_slope - exp_slope) < 1e-3, f"Slope mismatch. Expected {exp_slope:.4f}, got {act_slope:.4f}"
    assert abs(act_intercept - exp_intercept) < 1e-3, f"Intercept mismatch. Expected {exp_intercept:.4f}, got {act_intercept:.4f}"
    assert abs(act_rss - exp_rss) < 1e-3, f"RSS mismatch. Expected {exp_rss:.4f}, got {act_rss:.4f}"