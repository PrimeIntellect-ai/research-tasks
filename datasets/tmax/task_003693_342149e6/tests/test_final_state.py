# test_final_state.py
import os
import csv
import math

def get_robust_cov_corr(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = {h: [] for h in header}
        for row in reader:
            if not row: continue
            for h, v in zip(header, row):
                data[h].append(float(v))

    def mean(x):
        return sum(x) / len(x)

    def cov(x, y):
        n = len(x)
        mx = mean(x)
        my = mean(y)
        # Two-pass algorithm is numerically stable enough for this offset
        return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)

    cov_matrix = {}
    corr_matrix = {}

    for c1 in header:
        cov_matrix[c1] = {}
        corr_matrix[c1] = {}
        for c2 in header:
            c = cov(data[c1], data[c2])
            vx = cov(data[c1], data[c1])
            vy = cov(data[c2], data[c2])
            r = c / math.sqrt(vx * vy)
            cov_matrix[c1][c2] = round(c, 4)
            corr_matrix[c1][c2] = round(r, 4)

    return header, cov_matrix, corr_matrix

def read_matrix_csv(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)[1:] # First column is index
        matrix = {}
        for row in reader:
            if not row: continue
            idx = row[0]
            matrix[idx] = {}
            for h, v in zip(header, row[1:]):
                matrix[idx][h] = float(v)
    return header, matrix

def test_covariance_matrix():
    assert os.path.exists('/home/user/covariance.csv'), "/home/user/covariance.csv is missing."

    header, expected_cov, _ = get_robust_cov_corr('/home/user/sensordata.csv')
    out_header, out_cov = read_matrix_csv('/home/user/covariance.csv')

    assert out_header == header, "Covariance CSV columns do not match sensor data."

    for c1 in header:
        for c2 in header:
            expected = expected_cov[c1][c2]
            actual = out_cov[c1][c2]
            assert math.isclose(actual, expected, abs_tol=1e-4), f"Covariance mismatch for {c1}, {c2}: expected {expected}, got {actual}"

def test_correlation_matrix():
    assert os.path.exists('/home/user/correlation.csv'), "/home/user/correlation.csv is missing."

    header, _, expected_corr = get_robust_cov_corr('/home/user/sensordata.csv')
    out_header, out_corr = read_matrix_csv('/home/user/correlation.csv')

    assert out_header == header, "Correlation CSV columns do not match sensor data."

    for c1 in header:
        for c2 in header:
            expected = expected_corr[c1][c2]
            actual = out_corr[c1][c2]
            assert math.isclose(actual, expected, abs_tol=1e-4), f"Correlation mismatch for {c1}, {c2}: expected {expected}, got {actual}"

def test_heatmap_generated():
    heatmap_path = '/home/user/heatmap.png'
    assert os.path.exists(heatmap_path), f"{heatmap_path} is missing."

    size = os.path.getsize(heatmap_path)
    assert size > 1000, f"{heatmap_path} is too small ({size} bytes), likely broken or blank."

    with open(heatmap_path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"{heatmap_path} is not a valid PNG file."