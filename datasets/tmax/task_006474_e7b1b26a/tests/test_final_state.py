# test_final_state.py
import os
import csv
import math

def test_pipeline_exists():
    assert os.path.isfile("/home/user/pipeline.py"), "/home/user/pipeline.py does not exist."

def test_output_csv_exists():
    assert os.path.isfile("/home/user/output.csv"), "/home/user/output.csv does not exist."

def test_output_csv_content():
    expected_rows = [
        ["1", "10.5000", "19", "0.3015", "-0.3804"],
        ["2", "15.0000", "23", "0.3015", "-0.3804"],
        ["3", "20.0000", "31", "0.0000", "0.0000"],
        ["4", "12.5000", "26", "0.0000", "0.0000"],
        ["5", "9.9900", "36", "0.9070", "0.2529"]
    ]

    with open("/home/user/output.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["id", "price", "text_length", "emb_0", "emb_1"], "CSV header is incorrect. Expected: id, price, text_length, emb_0, emb_1"

        rows = list(reader)
        assert len(rows) == len(expected_rows), f"Incorrect number of rows in output.csv. Expected {len(expected_rows)}, got {len(rows)}."

        for i, (row, exp_row) in enumerate(zip(rows, expected_rows)):
            assert row[0] == exp_row[0], f"Row {i+1}: id mismatch."
            assert math.isclose(float(row[1]), float(exp_row[1]), abs_tol=1e-4), f"Row {i+1}: price mismatch."
            assert row[2] == exp_row[2], f"Row {i+1}: text_length mismatch."

            # Allow sign flips for embeddings as SVD solvers can flip signs depending on the architecture
            assert math.isclose(abs(float(row[3])), abs(float(exp_row[3])), abs_tol=1e-3), f"Row {i+1}: emb_0 magnitude mismatch. Expected ~{abs(float(exp_row[3]))}, got {abs(float(row[3]))}."
            assert math.isclose(abs(float(row[4])), abs(float(exp_row[4])), abs_tol=1e-3), f"Row {i+1}: emb_1 magnitude mismatch. Expected ~{abs(float(exp_row[4]))}, got {abs(float(row[4]))}."

def test_pipeline_code_constraints():
    with open("/home/user/pipeline.py", "r") as f:
        code = f.read()

    assert 'OPENBLAS_NUM_THREADS' in code, "OPENBLAS_NUM_THREADS not found in pipeline.py."
    assert '"1"' in code or "'1'" in code, "OPENBLAS_NUM_THREADS should be set to '1' in pipeline.py."

    openblas_pos = code.find('OPENBLAS_NUM_THREADS')

    np_pos = code.find('import numpy')
    if np_pos == -1:
        np_pos = code.find('from numpy')

    sk_pos = code.find('import sklearn')
    if sk_pos == -1:
        sk_pos = code.find('from sklearn')

    if np_pos != -1:
        assert openblas_pos < np_pos, "OPENBLAS_NUM_THREADS must be set before importing numpy."
    if sk_pos != -1:
        assert openblas_pos < sk_pos, "OPENBLAS_NUM_THREADS must be set before importing sklearn."