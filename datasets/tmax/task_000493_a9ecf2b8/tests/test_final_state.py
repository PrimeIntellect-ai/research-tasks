# test_final_state.py

import os
import json
import csv
import math

def get_cpu_median(filepath):
    """Compute the median of the cpu_usage column ignoring NaNs."""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        cpu_vals = []
        for row in reader:
            val = row.get('cpu_usage', '')
            if val.strip() != '' and val.strip().lower() != 'nan':
                try:
                    cpu_vals.append(float(val))
                except ValueError:
                    pass

    if not cpu_vals:
        return 0.0

    cpu_vals.sort()
    n = len(cpu_vals)
    if n % 2 == 1:
        return cpu_vals[n//2]
    else:
        return (cpu_vals[n//2 - 1] + cpu_vals[n//2]) / 2.0

def test_report_json_exists():
    """Test that the report.json file was created in the correct location."""
    file_path = '/home/user/report.json'
    assert os.path.exists(file_path), f"The file {file_path} does not exist. Ensure you saved your output."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_report_json_structure_and_values():
    """Test that the report.json contains the correct keys and accurately computed values."""
    file_path = '/home/user/report.json'
    with open(file_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} does not contain valid JSON."

    expected_keys = ["imputed_cpu_median", "pca_explained_variance_ratio", "brier_score"]
    for key in expected_keys:
        assert key in report, f"Key '{key}' is missing from {file_path}."

    # Validate imputed_cpu_median by recomputing it from the CSV
    csv_path = '/home/user/system_metrics.csv'
    expected_median = round(get_cpu_median(csv_path), 4)
    actual_median = report["imputed_cpu_median"]
    assert isinstance(actual_median, (int, float)), "imputed_cpu_median must be a float."
    assert math.isclose(actual_median, expected_median, abs_tol=1e-3), \
        f"imputed_cpu_median is incorrect. Expected ~{expected_median}, got {actual_median}."

    # Validate pca_explained_variance_ratio
    pca_evr = report["pca_explained_variance_ratio"]
    assert isinstance(pca_evr, list), "pca_explained_variance_ratio must be a list."
    assert len(pca_evr) == 2, "pca_explained_variance_ratio must contain exactly 2 elements."
    assert isinstance(pca_evr[0], (int, float)) and isinstance(pca_evr[1], (int, float)), \
        "Elements of pca_explained_variance_ratio must be floats."

    # Hardcoded expected values due to complex stdlib implementation of PCA
    expected_pca_0 = 0.2223
    expected_pca_1 = 0.2078
    assert math.isclose(pca_evr[0], expected_pca_0, abs_tol=1e-2), \
        f"First PCA explained variance ratio is incorrect. Expected ~{expected_pca_0}, got {pca_evr[0]}."
    assert math.isclose(pca_evr[1], expected_pca_1, abs_tol=1e-2), \
        f"Second PCA explained variance ratio is incorrect. Expected ~{expected_pca_1}, got {pca_evr[1]}."

    # Validate brier_score
    brier_score = report["brier_score"]
    assert isinstance(brier_score, (int, float)), "brier_score must be a float."

    # Hardcoded expected value due to complex stdlib implementation of GaussianNB
    expected_brier = 0.0264
    assert math.isclose(brier_score, expected_brier, abs_tol=1e-2), \
        f"brier_score is incorrect. Expected ~{expected_brier}, got {brier_score}."