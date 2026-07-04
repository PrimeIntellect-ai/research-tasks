# test_final_state.py
import os
import csv
import math
import pytest

def test_files_exist():
    assert os.path.exists('/home/user/correlation_matrix.csv'), "/home/user/correlation_matrix.csv is missing"
    assert os.path.exists('/home/user/heatmap.png'), "/home/user/heatmap.png is missing"

def test_heatmap_size():
    size = os.path.getsize('/home/user/heatmap.png')
    assert size > 2000, f"/home/user/heatmap.png seems empty/blank (size: {size} bytes)"

def test_correlation_matrix_content():
    # Read the generated CSV
    with open('/home/user/correlation_matrix.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        # First column is the index (might be empty string or 'Unnamed: 0')
        assert header[1:] == ['temp', 'pressure', 'humidity', 'vibration', 'light'], "Columns in correlation_matrix.csv are incorrect"

        rows = {}
        for row in reader:
            rows[row[0]] = [float(x) for x in row[1:]]

    # Expected index names
    expected_index = ['temp', 'pressure', 'humidity', 'vibration', 'light']
    for idx in expected_index:
        assert idx in rows, f"Row {idx} is missing from correlation_matrix.csv"

    # Compute expected correlation between temp and light
    temp = [20.5, 21.5, 22.0, 22.5, 23.0]
    light = [100.0, 110.0, 105.0, 120.0, 130.0]

    n = len(temp)
    mean_temp = sum(temp) / n
    mean_light = sum(light) / n

    num = sum((t - mean_temp) * (l - mean_light) for t, l in zip(temp, light))
    den_t = sum((t - mean_temp) ** 2 for t in temp)
    den_l = sum((l - mean_light) ** 2 for l in light)

    expected_corr = num / math.sqrt(den_t * den_l)

    # Get computed correlation from the file
    light_idx = header.index('light') - 1
    actual_corr = rows['temp'][light_idx]

    assert math.isclose(actual_corr, expected_corr, rel_tol=1e-4, abs_tol=1e-4), \
        f"Expected correlation between temp and light to be {expected_corr}, but got {actual_corr}"