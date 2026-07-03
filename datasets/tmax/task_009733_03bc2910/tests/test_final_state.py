# test_final_state.py

import os
import csv
import math
import pytest

def get_cleaned_data():
    csv_path = '/home/user/equipment_stats.csv'
    assert os.path.exists(csv_path), f"File {csv_path} is missing."

    temps = []
    pressures = []
    vibrations = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            temps.append(float(row['temp']))
            pressures.append(float(row['pressure']) if row['pressure'] else None)
            vibrations.append(float(row['vibration']))

    # 1. Impute missing pressure with median
    valid_p = sorted([p for p in pressures if p is not None])
    mid = len(valid_p) // 2
    if len(valid_p) % 2 == 0:
        median_p = (valid_p[mid - 1] + valid_p[mid]) / 2.0
    else:
        median_p = valid_p[mid]

    for i in range(len(pressures)):
        if pressures[i] is None:
            pressures[i] = median_p

    # 2. Remove rows where temp > 100
    t, p, v = [], [], []
    for i in range(len(temps)):
        if temps[i] <= 100:
            t.append(temps[i])
            p.append(pressures[i])
            v.append(vibrations[i])

    return t, p, v

def compute_pearson_corr(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den = math.sqrt(sum((xi - mean_x)**2 for xi in x) * sum((yi - mean_y)**2 for yi in y))
    return num / den

def compute_linear_regression(t, p, v):
    n = len(t)
    sum_t = sum(t)
    sum_p = sum(p)
    sum_t2 = sum(ti**2 for ti in t)
    sum_p2 = sum(pi**2 for pi in p)
    sum_tp = sum(ti*pi for ti, pi in zip(t, p))

    sum_v = sum(v)
    sum_tv = sum(ti*vi for ti, vi in zip(t, v))
    sum_pv = sum(pi*vi for pi, vi in zip(p, v))

    # 3x3 matrix for Normal Equations: X^T X
    m = [
        [sum_t2, sum_tp, sum_t],
        [sum_tp, sum_p2, sum_p],
        [sum_t,  sum_p,  n]
    ]

    # Determinant of 3x3
    det = m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - \
          m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + \
          m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])

    # Inverse of 3x3 (only need first two rows for coefficients of t and p)
    inv00 = (m[1][1] * m[2][2] - m[1][2] * m[2][1]) / det
    inv01 = (m[0][2] * m[2][1] - m[0][1] * m[2][2]) / det
    inv02 = (m[0][1] * m[1][2] - m[0][2] * m[1][1]) / det

    inv10 = (m[1][2] * m[2][0] - m[1][0] * m[2][2]) / det
    inv11 = (m[0][0] * m[2][2] - m[0][2] * m[2][0]) / det
    inv12 = (m[0][2] * m[1][0] - m[0][0] * m[1][2]) / det

    coef_t = inv00*sum_tv + inv01*sum_pv + inv02*sum_v
    coef_p = inv10*sum_tv + inv11*sum_pv + inv12*sum_v

    return coef_t, coef_p

def test_metrics_log_contents():
    log_path = '/home/user/metrics.log'
    assert os.path.exists(log_path), f"File {log_path} does not exist. The script may not have run successfully."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, but found {len(lines)}."

    t, p, v = get_cleaned_data()

    expected_corr = compute_pearson_corr(t, p)
    expected_coef_t, expected_coef_p = compute_linear_regression(t, p, v)

    expected_line1 = f"{expected_corr:.4f}"
    expected_line2 = f"{expected_coef_t:.4f},{expected_coef_p:.4f}"

    assert lines[0] == expected_line1, f"Line 1 (correlation) mismatch. Expected '{expected_line1}', got '{lines[0]}'."
    assert lines[1] == expected_line2, f"Line 2 (coefficients) mismatch. Expected '{expected_line2}', got '{lines[1]}'."