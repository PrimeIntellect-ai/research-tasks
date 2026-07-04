# test_final_state.py
import os

def test_notebook_exists():
    notebook_path = "/home/user/analyze_structure.ipynb"
    assert os.path.exists(notebook_path), f"The Jupyter notebook {notebook_path} does not exist."
    assert os.path.isfile(notebook_path), f"{notebook_path} is not a file."

def test_singular_values_file_exists():
    output_path = "/home/user/singular_values.txt"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_singular_values_contents():
    output_path = "/home/user/singular_values.txt"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 singular values, but found {len(lines)}."

    expected_values = ["3.8569", "1.9213", "0.0000"]
    for i, (actual, expected) in enumerate(zip(lines, expected_values)):
        assert actual == expected, f"Line {i+1} mismatch: expected {expected}, got {actual}."