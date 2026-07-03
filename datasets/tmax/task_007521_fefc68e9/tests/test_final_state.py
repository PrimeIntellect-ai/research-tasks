# test_final_state.py

import os
import csv
import math
import pytest

CSV_PATH = "/home/user/artifacts/pca_projection.csv"

def test_artifacts_dir_and_csv_exist():
    assert os.path.exists("/home/user/artifacts"), "The artifacts directory does not exist."
    assert os.path.isfile(CSV_PATH), f"The output file {CSV_PATH} does not exist."

def test_csv_structure_and_sorting():
    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['run_id', 'pca_1', 'pca_2'], f"Expected header ['run_id', 'pca_1', 'pca_2'], but got {header}"

        rows = list(reader)
        assert len(rows) == 5, f"Expected 5 rows of data, but got {len(rows)}"

        run_ids = [row[0] for row in rows]
        expected_run_ids = ['run_A', 'run_B', 'run_C', 'run_D', 'run_E']
        assert run_ids == expected_run_ids, f"Expected run_ids to be sorted as {expected_run_ids}, but got {run_ids}"

def test_pca_coordinates_distances():
    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        coords = []
        for row in reader:
            try:
                pca_1 = float(row['pca_1'])
                pca_2 = float(row['pca_2'])
                coords.append((pca_1, pca_2))
            except ValueError:
                pytest.fail(f"Could not parse PCA coordinates as floats for run_id {row.get('run_id')}")

    # Expected pairwise distances based on standardized PCA of the given dataset
    expected_distances = [
        [0.0, 1.2599, 3.2514, 1.4878, 4.4568],
        [1.2599, 0.0, 1.9962, 2.7317, 3.2104],
        [3.2514, 1.9962, 0.0, 4.7001, 1.2185],
        [1.4878, 2.7317, 4.7001, 0.0, 5.9181],
        [4.4568, 3.2104, 1.2185, 5.9181, 0.0]
    ]

    for i in range(len(coords)):
        for j in range(len(coords)):
            dist = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
            expected_dist = expected_distances[i][j]
            assert abs(dist - expected_dist) < 0.01, (
                f"Distance between point {i} and {j} is {dist:.4f}, "
                f"expected {expected_dist:.4f}. PCA results do not match expected projection."
            )