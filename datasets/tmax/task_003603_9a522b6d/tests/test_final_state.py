# test_final_state.py

import os
import csv
import math
import pytest

RESULTS_FILE = '/home/user/results/gene_fits.csv'

def test_results_file_exists():
    """Test that the results CSV file has been created."""
    assert os.path.isfile(RESULTS_FILE), f"Expected output file {RESULTS_FILE} does not exist."

def test_csv_headers():
    """Test that the CSV file has the exact required columns."""
    assert os.path.isfile(RESULTS_FILE), f"Expected output file {RESULTS_FILE} does not exist."
    with open(RESULTS_FILE, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"File {RESULTS_FILE} is empty.")

    expected_headers = ['gene_id', 'amplitude', 'period', 'phase', 'baseline']
    assert headers == expected_headers, f"Expected headers {expected_headers}, but got {headers}."

def test_csv_sorting_and_rounding():
    """Test that the rows are sorted alphabetically by gene_id and values are rounded to 3 decimal places."""
    assert os.path.isfile(RESULTS_FILE), f"Expected output file {RESULTS_FILE} does not exist."
    with open(RESULTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    gene_ids = [row['gene_id'] for row in rows]
    assert gene_ids == sorted(gene_ids), "The rows are not sorted alphabetically by gene_id."

    for row in rows:
        for col in ['amplitude', 'period', 'phase', 'baseline']:
            val_str = row[col]
            # Check if it has exactly 3 decimal places
            if '.' in val_str:
                decimals = val_str.split('.')[1]
                assert len(decimals) == 3, f"Value {val_str} for {col} in gene {row['gene_id']} is not rounded to exactly 3 decimal places."
            else:
                pytest.fail(f"Value {val_str} for {col} in gene {row['gene_id']} does not have decimal places.")

def test_csv_values():
    """Test that the fitted values are within the acceptable tolerance of the expected values."""
    assert os.path.isfile(RESULTS_FILE), f"Expected output file {RESULTS_FILE} does not exist."

    expected = {
        'BMAL1': {'amplitude': 15.143, 'period': 23.829, 'phase': 3.962, 'baseline': 29.870},
        'CLOCK': {'amplitude': 4.909, 'period': 24.536, 'phase': 2.443, 'baseline': 15.035},
        'PER1': {'amplitude': 9.873, 'period': 24.150, 'phase': 0.942, 'baseline': 20.010}
    }

    with open(RESULTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 3, f"Expected exactly 3 rows of data, got {len(rows)}."

    for row in rows:
        g = row['gene_id']
        assert g in expected, f"Unexpected gene_id {g} in results."

        try:
            amp = float(row['amplitude'])
            period = float(row['period'])
            phase = float(row['phase'])
            baseline = float(row['baseline'])
        except ValueError as e:
            pytest.fail(f"Could not parse numeric values for gene {g}: {e}")

        assert abs(amp - expected[g]['amplitude']) < 0.1, f"Amplitude for {g} is {amp}, expected ~{expected[g]['amplitude']}."
        assert abs(period - expected[g]['period']) < 0.1, f"Period for {g} is {period}, expected ~{expected[g]['period']}."
        assert abs(phase - expected[g]['phase']) < 0.1, f"Phase for {g} is {phase}, expected ~{expected[g]['phase']}."
        assert abs(baseline - expected[g]['baseline']) < 0.1, f"Baseline for {g} is {baseline}, expected ~{expected[g]['baseline']}."