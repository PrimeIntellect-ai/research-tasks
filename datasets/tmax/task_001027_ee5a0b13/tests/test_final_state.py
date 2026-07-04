# test_final_state.py
import os
import csv
import math

def test_script_modified():
    script_path = "/home/user/generate_features.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "solve_ivp" in content, "The script does not appear to use scipy.integrate.solve_ivp as requested."
    assert "BDF" in content, "The script does not appear to use the 'BDF' method for solve_ivp."

def test_csv_output():
    csv_path = "/home/user/training_features.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist. Did you run the script?"

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        expected_header = ["Sequence", "Integration", "SVD", "Alignment"]
        assert header == expected_header, f"Incorrect CSV header. Expected {expected_header}, got {header}."

        rows = list(reader)
        assert len(rows) == 4, f"Expected 4 rows of data, found {len(rows)}."

        for row in rows:
            assert len(row) == 4, f"Row does not have exactly 4 columns: {row}"
            seq, integration, svd, alignment = row

            try:
                int_val = float(integration)
            except ValueError:
                assert False, f"Integration value '{integration}' is not a valid float."

            assert not math.isnan(int_val), f"Integration value for sequence {seq} is NaN."
            assert not math.isinf(int_val), f"Integration value for sequence {seq} is Inf."

            try:
                float(svd)
                float(alignment)
            except ValueError:
                assert False, f"SVD or Alignment values are not valid floats in row: {row}"