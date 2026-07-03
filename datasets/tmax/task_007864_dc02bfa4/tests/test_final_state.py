# test_final_state.py

import os
import csv
import math
import pytest

def pearson_corr(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / math.sqrt(den_x * den_y)

def test_clean_data_exists():
    assert os.path.isfile("/home/user/results/clean_data.csv"), "clean_data.csv was not created in /home/user/results/"

def test_clean_data_schema_and_pca():
    filepath = "/home/user/results/clean_data.csv"
    assert os.path.isfile(filepath), "clean_data.csv is missing"

    categories = []
    pca_1 = []
    pca_2 = []
    targets = []

    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat_str = row['category']
            assert cat_str.strip() != "", "Found empty (NaN) value in category column"

            # This will raise ValueError if it's a float like '1.0' instead of '1'
            # But pandas writing int64 will write standard integers.
            try:
                cat_val = int(cat_str)
                # If pandas wrote '10.0', int('10.0') fails, which correctly enforces strict int formatting
            except ValueError:
                # If it's a float string like '-1.0', we fail it
                pytest.fail(f"Category value '{cat_str}' is not formatted as a strict integer (int64).")

            categories.append(cat_val)
            pca_1.append(float(row['pca_1']))
            pca_2.append(float(row['pca_2']))
            targets.append(float(row['target']))

    assert -1 in categories, "-1 was not found in the category column (999 should be replaced with -1)"
    assert 999 not in categories, "999 is still present in the category column"

    # Test PCA centering and orthogonality
    n = len(pca_1)
    mean_pca_1 = sum(pca_1) / n
    mean_pca_2 = sum(pca_2) / n

    assert abs(mean_pca_1) < 1e-5, f"pca_1 is not mean-centered (mean = {mean_pca_1}). Did you subtract the mean before projection?"
    assert abs(mean_pca_2) < 1e-5, f"pca_2 is not mean-centered (mean = {mean_pca_2}). Did you subtract the mean before projection?"

    dot_product = sum(p1 * p2 for p1, p2 in zip(pca_1, pca_2))
    assert abs(dot_product) < 1e-4, f"pca_1 and pca_2 are not orthogonal (dot product = {dot_product}). PCA implementation is incorrect."

def test_correlation_output():
    corr_filepath = "/home/user/results/abs_corr_pca1_target.txt"
    assert os.path.isfile(corr_filepath), "abs_corr_pca1_target.txt was not created"

    with open(corr_filepath, 'r') as f:
        content = f.read().strip()
        try:
            reported_corr = float(content)
        except ValueError:
            pytest.fail(f"Content of abs_corr_pca1_target.txt is not a valid float: {content}")

    # Recompute correlation from the clean_data.csv
    filepath = "/home/user/results/clean_data.csv"
    assert os.path.isfile(filepath), "clean_data.csv is missing"

    pca_1 = []
    targets = []
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pca_1.append(float(row['pca_1']))
            targets.append(float(row['target']))

    actual_corr = abs(pearson_corr(pca_1, targets))
    expected_corr_rounded = round(actual_corr, 4)

    assert abs(reported_corr - expected_corr_rounded) < 1e-4, f"Correlation value mismatch. Expected {expected_corr_rounded}, got {reported_corr}"