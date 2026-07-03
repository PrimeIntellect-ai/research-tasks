# test_final_state.py

import os
import csv
import math
import pytest

def test_pca_plot_exists():
    plot_path = '/home/user/output/pca_plot.png'
    assert os.path.isfile(plot_path), f"The plot file {plot_path} is missing. Ensure the script correctly saves the plot."
    assert os.path.getsize(plot_path) > 0, f"The plot file {plot_path} is empty."

def test_pca_results_exists_and_format():
    results_path = '/home/user/output/pca_results.csv'
    assert os.path.isfile(results_path), f"The results file {results_path} is missing."

    with open(results_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['server_id', 'pc1', 'pc2'], f"The header in {results_path} is incorrect. Expected ['server_id', 'pc1', 'pc2'], got {header}."

        rows = list(reader)
        assert len(rows) == 3, f"Expected 3 rows of data, got {len(rows)}."

        server_ids = [row[0] for row in rows]
        assert server_ids == ['srv_01', 'srv_02', 'srv_03'], f"The rows should be sorted ascending by server_id. Got {server_ids}."

def test_pca_results_values():
    results_path = '/home/user/output/pca_results.csv'
    assert os.path.isfile(results_path), "The results file is missing."

    expected_abs_pc1 = {
        'srv_01': 0.10177708307221651,
        'srv_02': 2.120353065099309,
        'srv_03': 2.2221301481715266
    }

    expected_abs_pc2 = {
        'srv_01': 0.06326694672051286,
        'srv_02': 0.021028741369766943,
        'srv_03': 0.08429568809028017
    }

    with open(results_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        server_id = row['server_id']
        pc1 = float(row['pc1'])
        pc2 = float(row['pc2'])

        # Check absolute values to account for PCA sign flips
        assert math.isclose(abs(pc1), expected_abs_pc1[server_id], rel_tol=1e-4), \
            f"PC1 value for {server_id} is incorrect. Expected abs value ~{expected_abs_pc1[server_id]}, got {pc1}."

        assert math.isclose(abs(pc2), expected_abs_pc2[server_id], rel_tol=1e-4), \
            f"PC2 value for {server_id} is incorrect. Expected abs value ~{expected_abs_pc2[server_id]}, got {pc2}."