# test_final_state.py
import os

def test_c_source_file_exists():
    file_path = '/home/user/analyze_graph.c'
    assert os.path.exists(file_path), f"C source file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_csv_output_exists():
    file_path = '/home/user/top_datasets.csv'
    assert os.path.exists(file_path), f"Output CSV file {file_path} is missing. Did the program run successfully?"
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_csv_output_content():
    file_path = '/home/user/top_datasets.csv'
    expected_csv = """astronomy,ds08,2,1
astronomy,ds09,2,2
astronomy,ds10,2,3
genomics,ds01,3,1
genomics,ds03,2,2
genomics,ds02,1,3
physics,ds05,4,1
physics,ds04,2,2
physics,ds06,1,3"""

    expected_lines = sorted([line.strip() for line in expected_csv.strip().split('\n')])

    with open(file_path, 'r') as f:
        actual_lines = sorted([line.strip() for line in f.read().strip().split('\n') if line.strip()])

    assert actual_lines == expected_lines, (
        f"CSV content does not match expected output.\n"
        f"Expected (sorted):\n{expected_lines}\n"
        f"Actual (sorted):\n{actual_lines}"
    )