# test_final_state.py
import os
import csv
import math

def test_scatter_plot_exists():
    plot_path = '/home/user/scatter.png'
    assert os.path.isfile(plot_path), f"Expected plot file {plot_path} does not exist."
    assert os.path.getsize(plot_path) > 1000, f"Plot file {plot_path} is too small to be a valid image."

def get_percentile(data, q):
    if not data:
        return None
    data = sorted(data)
    n = len(data)
    p = (n - 1) * q
    i = int(p)
    f = p - i
    if i + 1 < n:
        return (1 - f) * data[i] + f * data[i + 1]
    else:
        return data[i]

def test_cleaned_data_correct():
    raw_path = '/home/user/raw_data.csv'
    cleaned_path = '/home/user/cleaned_data.csv'

    assert os.path.isfile(cleaned_path), f"Expected cleaned data file {cleaned_path} does not exist."

    with open(raw_path, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)

        try:
            idx_a = headers.index('A')
            idx_b = headers.index('B')
            idx_c = headers.index('C')
        except ValueError as e:
            assert False, f"Raw data missing required columns: {e}"

        raw_rows = list(reader)

    # 1. Drop rows where A is NaN
    filtered_rows = []
    for row in raw_rows:
        val_a = row[idx_a]
        if val_a.strip().lower() in ('', 'nan'):
            continue
        filtered_rows.append(row)

    # 2. Fill missing B with mean of remaining B
    b_values = []
    for row in filtered_rows:
        val_b = row[idx_b]
        if val_b.strip().lower() not in ('', 'nan'):
            b_values.append(float(val_b))

    b_mean = sum(b_values) / len(b_values) if b_values else 0.0

    # 3. Clip C to 5th and 95th percentiles
    c_values = []
    for row in filtered_rows:
        val_c = row[idx_c]
        if val_c.strip().lower() not in ('', 'nan'):
            c_values.append(float(val_c))

    p5 = get_percentile(c_values, 0.05)
    p95 = get_percentile(c_values, 0.95)

    expected_data = []
    for row in filtered_rows:
        a = float(row[idx_a])

        val_b = row[idx_b]
        if val_b.strip().lower() in ('', 'nan'):
            b = b_mean
        else:
            b = float(val_b)

        val_c = row[idx_c]
        if val_c.strip().lower() in ('', 'nan'):
            c = float('nan')
        else:
            c = float(val_c)
            if c < p5:
                c = p5
            elif c > p95:
                c = p95

        expected_data.append((a, b, c))

    # Read cleaned data and verify
    with open(cleaned_path, 'r', newline='') as f:
        reader = csv.reader(f)
        cleaned_headers = next(reader)
        assert cleaned_headers == ['A', 'B', 'C'], f"Cleaned data headers should be ['A', 'B', 'C'], got {cleaned_headers}"

        cleaned_rows = list(reader)

    assert len(cleaned_rows) == len(expected_data), f"Expected {len(expected_data)} rows in cleaned data, got {len(cleaned_rows)}"

    for i, (exp, act) in enumerate(zip(expected_data, cleaned_rows)):
        try:
            act_a, act_b, act_c = float(act[0]), float(act[1]), float(act[2])
        except ValueError:
            assert False, f"Row {i+1} in cleaned data contains non-float values: {act}"

        assert math.isclose(act_a, exp[0], rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} Col A mismatch: expected {exp[0]}, got {act_a}"
        assert math.isclose(act_b, exp[1], rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} Col B mismatch: expected {exp[1]}, got {act_b}"
        assert math.isclose(act_c, exp[2], rel_tol=1e-4, abs_tol=1e-4), f"Row {i+1} Col C mismatch: expected {exp[2]}, got {act_c}"