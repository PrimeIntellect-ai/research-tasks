# test_final_state.py

import os
import csv

def test_eigen_extracted():
    """Test that the Eigen library was downloaded and extracted."""
    eigen_path = '/home/user/eigen/eigen-3.4.0/Eigen'
    assert os.path.isdir(eigen_path), f"Eigen library directory {eigen_path} not found. Did you extract it correctly?"

def test_cpp_file_exists():
    """Test that the C++ source file was created."""
    cpp_file = '/home/user/etl_pipeline.cpp'
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_processed_data_exists():
    """Test that the output CSV file was created."""
    output_file = '/home/user/processed_data.csv'
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did the C++ program run successfully?"

def test_processed_data_format():
    """Test that the output CSV has the correct dimensions and data types."""
    output_file = '/home/user/processed_data.csv'
    if not os.path.isfile(output_file):
        return # Handled by previous test

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 7, f"Expected 7 rows in the output data, but got {len(rows)}."

    for i, row in enumerate(rows):
        assert len(row) == 2, f"Expected 2 columns (top 2 principal components) in row {i+1}, but got {len(row)}."
        for j, val in enumerate(row):
            try:
                float(val)
            except ValueError:
                assert False, f"Value '{val}' in row {i+1}, column {j+1} is not a valid float."

def test_processed_data_mean_centered():
    """
    Test that the output data is roughly mean-centered, 
    which is a property of projected PCA data when the original data was mean-centered.
    """
    output_file = '/home/user/processed_data.csv'
    if not os.path.isfile(output_file):
        return

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    col1 = [float(row[0]) for row in rows]
    col2 = [float(row[1]) for row in rows]

    mean1 = sum(col1) / len(col1)
    mean2 = sum(col2) / len(col2)

    assert abs(mean1) < 1e-3, f"Expected column 1 mean to be close to 0, got {mean1}"
    assert abs(mean2) < 1e-3, f"Expected column 2 mean to be close to 0, got {mean2}"