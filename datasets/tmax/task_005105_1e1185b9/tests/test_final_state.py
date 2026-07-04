# test_final_state.py

import os
import csv
import re
import pytest

def test_combined_csv_exists_and_correct():
    csv_path = "/home/user/data/combined.csv"
    assert os.path.isfile(csv_path), f"Expected CSV file {csv_path} does not exist."

    expected_rows = [
        {"index": "1", "fasta_char": "A", "pdb_res_name": "ALA", "b_factor": "20.50"},
        {"index": "2", "fasta_char": "R", "pdb_res_name": "ARG", "b_factor": "23.50"},
        {"index": "3", "fasta_char": "N", "pdb_res_name": "ASN", "b_factor": "26.50"},
        {"index": "4", "fasta_char": "D", "pdb_res_name": "ASP", "b_factor": "29.50"},
        {"index": "5", "fasta_char": "C", "pdb_res_name": "CYS", "b_factor": "32.50"},
    ]

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None, "CSV must have a header."

        # Check header fields
        expected_fields = ["index", "fasta_char", "pdb_res_name", "b_factor"]
        for field in expected_fields:
            assert field in reader.fieldnames, f"CSV header missing expected column: {field}"

        rows = list(reader)
        assert len(rows) == len(expected_rows), f"CSV should have exactly {len(expected_rows)} data rows, found {len(rows)}."

        for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
            assert actual["index"].strip() == expected["index"], f"Row {i+1} index mismatch."
            assert actual["fasta_char"].strip() == expected["fasta_char"], f"Row {i+1} fasta_char mismatch."
            assert actual["pdb_res_name"].strip() == expected["pdb_res_name"], f"Row {i+1} pdb_res_name mismatch."

            # Allow float comparison for b_factor
            actual_b = float(actual["b_factor"].strip())
            expected_b = float(expected["b_factor"])
            assert abs(actual_b - expected_b) < 1e-4, f"Row {i+1} b_factor mismatch: expected {expected_b}, got {actual_b}."

def test_model_results_exist_and_correct():
    results_path = "/home/user/output/model_results.txt"
    assert os.path.isfile(results_path), f"Expected output file {results_path} does not exist."

    with open(results_path, "r") as f:
        content = f.read()

    alpha_match = re.search(r"alpha:\s*([+-]?\d*\.\d+)", content)
    beta_match = re.search(r"beta:\s*([+-]?\d*\.\d+)", content)

    assert alpha_match is not None, "Could not find 'alpha: <value>' in model_results.txt"
    assert beta_match is not None, "Could not find 'beta: <value>' in model_results.txt"

    alpha_val = float(alpha_match.group(1))
    beta_val = float(beta_match.group(1))

    # The expected fit is alpha = 17.5, beta = 3.0
    # Using a small tolerance for floating point and gradient descent convergence differences
    assert abs(alpha_val - 17.5) < 0.1, f"Alpha value {alpha_val} is not close enough to expected 17.5000"
    assert abs(beta_val - 3.0) < 0.1, f"Beta value {beta_val} is not close enough to expected 3.0000"