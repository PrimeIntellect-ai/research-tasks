# test_final_state.py

import os
import pytest

PROCESSED_DIR = "/home/user/data/processed"
PCA_CSV_PATH = os.path.join(PROCESSED_DIR, "pca_features.csv")
VAR_TXT_PATH = os.path.join(PROCESSED_DIR, "explained_variance.txt")

def test_processed_files_exist():
    """Test that the required output files exist."""
    assert os.path.exists(PCA_CSV_PATH), f"Failure: {PCA_CSV_PATH} missing"
    assert os.path.isfile(PCA_CSV_PATH), f"Failure: {PCA_CSV_PATH} is not a file"

    assert os.path.exists(VAR_TXT_PATH), f"Failure: {VAR_TXT_PATH} missing"
    assert os.path.isfile(VAR_TXT_PATH), f"Failure: {VAR_TXT_PATH} is not a file"

def test_pca_features_csv_format():
    """Test that the pca_features.csv has the correct headers and row count."""
    with open(PCA_CSV_PATH, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 298, f"Failure: Expected 298 lines in pca_features.csv, got {len(lines)}"

    expected_header = "timestamp,machine_id,PC1,PC2,PC3"
    assert lines[0] == expected_header, f"Failure: Incorrect headers in pca_features.csv. Expected '{expected_header}', got '{lines[0]}'"

    # Check that there are 5 columns in the data rows
    for i, line in enumerate(lines[1:], start=2):
        cols = line.split(",")
        assert len(cols) == 5, f"Failure: Row {i} in pca_features.csv does not have 5 columns."

def test_explained_variance_txt_format():
    """Test that the explained_variance.txt has exactly three comma-separated float values."""
    with open(VAR_TXT_PATH, "r") as f:
        content = f.read().strip()

    values = content.split(",")
    assert len(values) == 3, f"Failure: Expected 3 comma-separated values in explained_variance.txt, got {len(values)}"

    for val in values:
        try:
            float(val)
        except ValueError:
            pytest.fail(f"Failure: Value '{val}' in explained_variance.txt is not a valid float.")