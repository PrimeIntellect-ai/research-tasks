# test_final_state.py
import os
import csv
import math
import pytest

def test_training_features_exists_and_format():
    """Check if training_features.csv exists and has the correct format."""
    file_path = "/home/user/training_features.csv"
    assert os.path.isfile(file_path), f"Missing output file: {file_path}"

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["StrainID", "r", "K"], f"Incorrect header in {file_path}. Expected ['StrainID', 'r', 'K'], got {header}"

        rows = list(reader)
        assert len(rows) == 3, f"Expected 3 rows of data, got {len(rows)}"

        strains = [row[0] for row in rows]
        assert strains == ["Strain_Alpha", "Strain_Beta", "Strain_Gamma"], f"Strains are not sorted alphabetically or missing: {strains}"

def test_training_features_values():
    """Check if the fitted parameters r and K are within the expected tolerance."""
    file_path = "/home/user/training_features.csv"
    assert os.path.isfile(file_path), f"Missing output file: {file_path}"

    # Expected approximate values based on deterministic noise
    expected = {
        "Strain_Alpha": {"r": 0.662, "K": 1.222},
        "Strain_Beta": {"r": 0.404, "K": 0.844},
        "Strain_Gamma": {"r": 0.898, "K": 1.597}
    }

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            strain = row["StrainID"]
            assert strain in expected, f"Unexpected StrainID: {strain}"

            try:
                r_val = float(row["r"])
                k_val = float(row["K"])
            except ValueError:
                pytest.fail(f"Non-numeric values found for {strain}: r={row['r']}, K={row['K']}")

            expected_r = expected[strain]["r"]
            expected_k = expected[strain]["K"]

            # Tolerance is 5% of the expected value
            r_tol = expected_r * 0.05
            k_tol = expected_k * 0.05

            assert math.isclose(r_val, expected_r, abs_tol=r_tol), f"r value for {strain} is {r_val}, expected ~{expected_r}"
            assert math.isclose(k_val, expected_k, abs_tol=k_tol), f"K value for {strain} is {k_val}, expected ~{expected_k}"

def test_growth_fits_png_exists():
    """Check if growth_fits.png exists and is a non-empty file."""
    file_path = "/home/user/growth_fits.png"
    assert os.path.isfile(file_path), f"Missing image file: {file_path}"
    assert os.path.getsize(file_path) > 0, f"Image file {file_path} is empty"

    # Basic magic number check for PNG
    with open(file_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {file_path} is not a valid PNG image"