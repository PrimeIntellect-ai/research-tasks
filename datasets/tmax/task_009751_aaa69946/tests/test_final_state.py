# test_final_state.py
import os
import csv

def test_features_csv_exists():
    assert os.path.isfile('/home/user/features.csv'), "/home/user/features.csv is missing."

def test_features_csv_structure_and_content():
    filepath = '/home/user/features.csv'
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 101, f"Expected 101 rows (header + 100 data rows), found {len(rows)}"

    header = rows[0]
    assert header == ['filename', 'A', 'mu', 'sigma'], f"Incorrect header: {header}"

    data_rows = rows[1:]

    # Check sorting and filenames
    expected_filenames = [f"spec_{i:03d}.txt" for i in range(100)]
    actual_filenames = [row[0] for row in data_rows]
    assert actual_filenames == expected_filenames, "Filenames are not sorted or do not match the expected spec_XXX.txt format."

    # Check values
    for row in data_rows:
        assert len(row) == 4, f"Row {row[0]} does not have exactly 4 columns."

        filename, a_str, mu_str, sigma_str = row

        try:
            a = float(a_str)
            mu = float(mu_str)
            sigma = float(sigma_str)
        except ValueError:
            assert False, f"Non-numeric values found in row for {filename}: {row}"

        # Check formatting (rounded to 2 decimal places)
        # Note: rounding to 2 decimal places means at most 2 decimal places, or exactly 2.
        # We check if the string representation matches the rounded value to 2 decimal places.
        assert a_str == f"{a:.2f}" or a_str == str(round(a, 2)), f"Value A ({a_str}) not rounded to 2 decimal places in {filename}."
        assert mu_str == f"{mu:.2f}" or mu_str == str(round(mu, 2)), f"Value mu ({mu_str}) not rounded to 2 decimal places in {filename}."
        assert sigma_str == f"{sigma:.2f}" or sigma_str == str(round(sigma, 2)), f"Value sigma ({sigma_str}) not rounded to 2 decimal places in {filename}."

        # Check reasonable bounds based on the data generation (A~[5,15], mu~[500,700], sigma~[10,30])
        assert 0 < a < 50, f"Value A ({a}) out of reasonable bounds for {filename}."
        assert 400 <= mu <= 800, f"Value mu ({mu}) out of reasonable bounds for {filename}."
        assert 0 < sigma < 100, f"Value sigma ({sigma}) out of reasonable bounds for {filename}."