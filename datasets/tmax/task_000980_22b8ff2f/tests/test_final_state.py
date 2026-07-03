# test_final_state.py
import os
import csv
import re
import pytest

def compute_expected_values():
    # Read reference
    ref_path = "/home/user/data/reference.csv"
    raw_path = "/home/user/data/raw.csv"

    if not os.path.exists(ref_path) or not os.path.exists(raw_path):
        return None

    ref_signals = []
    with open(ref_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref_signals.append(float(row['signal']))

    raw_data = []
    with open(raw_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_data.append((float(row['time']), float(row['signal'])))

    # 1D Wasserstein Distance
    ref_sorted = sorted(ref_signals)
    raw_sorted = sorted([sig for _, sig in raw_data])
    wasserstein = sum(abs(r - w) for r, w in zip(ref_sorted, raw_sorted)) / len(ref_sorted)

    # Regression
    n = len(raw_data)
    mean_x = sum(t for t, _ in raw_data) / n
    mean_y = sum(sig for _, sig in raw_data) / n

    cov = sum((t - mean_x) * (sig - mean_y) for t, sig in raw_data)
    var = sum((t - mean_x) ** 2 for t, _ in raw_data)

    m = cov / var
    c = mean_y - m * mean_x

    # Residuals & Filtering
    cleaned_rows = []
    for t, sig in raw_data:
        pred = m * t + c
        residual = sig - pred
        if abs(residual) <= 2.0:
            cleaned_rows.append((t, sig))

    return {
        'wasserstein': wasserstein,
        'm': m,
        'c': c,
        'cleaned_count': len(cleaned_rows),
        'cleaned_rows': cleaned_rows
    }

def test_report_content():
    report_path = "/home/user/report.md"
    assert os.path.isfile(report_path), f"Report file missing at {report_path}"

    expected = compute_expected_values()
    assert expected is not None, "Initial data files missing, cannot compute expected values."

    with open(report_path, 'r') as f:
        content = f.read()

    # Check for the expected values formatted to two decimal places
    expected_w_str = f"{expected['wasserstein']:.2f}"
    expected_m_str = f"{expected['m']:.2f}"
    expected_c_str = f"{expected['c']:.2f}"
    expected_count_str = str(expected['cleaned_count'])

    assert re.search(r"- 1D Wasserstein Distance:\s*" + re.escape(expected_w_str), content), \
        f"Report missing or incorrect 1D Wasserstein Distance. Expected: {expected_w_str}"

    assert re.search(r"- Regression Slope \(m\):\s*" + re.escape(expected_m_str), content), \
        f"Report missing or incorrect Regression Slope (m). Expected: {expected_m_str}"

    assert re.search(r"- Regression Intercept \(c\):\s*" + re.escape(expected_c_str), content), \
        f"Report missing or incorrect Regression Intercept (c). Expected: {expected_c_str}"

    assert re.search(r"- Cleaned Rows Retained:\s*" + re.escape(expected_count_str), content), \
        f"Report missing or incorrect Cleaned Rows Retained. Expected: {expected_count_str}"

def test_cleaned_csv_content():
    cleaned_path = "/home/user/data/cleaned.csv"
    assert os.path.isfile(cleaned_path), f"Cleaned CSV file missing at {cleaned_path}"

    expected = compute_expected_values()
    assert expected is not None, "Initial data files missing, cannot compute expected values."

    actual_rows = []
    with open(cleaned_path, 'r') as f:
        reader = csv.DictReader(f)
        assert 'time' in reader.fieldnames and 'signal' in reader.fieldnames, \
            "Cleaned CSV header must contain 'time' and 'signal'"
        for row in reader:
            actual_rows.append((float(row['time']), float(row['signal'])))

    assert len(actual_rows) == expected['cleaned_count'], \
        f"Cleaned CSV should have {expected['cleaned_count']} rows, found {len(actual_rows)}"

    # Check values with a small tolerance for float formatting
    for expected_row, actual_row in zip(expected['cleaned_rows'], actual_rows):
        assert abs(expected_row[0] - actual_row[0]) < 1e-6, \
            f"Time value mismatch in cleaned.csv: expected {expected_row[0]}, got {actual_row[0]}"
        assert abs(expected_row[1] - actual_row[1]) < 1e-6, \
            f"Signal value mismatch in cleaned.csv: expected {expected_row[1]}, got {actual_row[1]}"