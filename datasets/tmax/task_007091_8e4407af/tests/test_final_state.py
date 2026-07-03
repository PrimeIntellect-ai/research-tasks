# test_final_state.py
import os

def test_cleaned_edges_csv():
    file_path = "/home/user/cleaned_edges.csv"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read()

    assert "CROSS_JOIN_ERROR" not in content, "The cleaned_edges.csv file still contains 'CROSS_JOIN_ERROR' lines."
    assert "NODE_001,NODE_100" in content, "The cleaned_edges.csv file is missing valid edges."

def test_shortest_path_script():
    file_path = "/home/user/shortest_path.py"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."
    assert os.access(file_path, os.X_OK), f"The script {file_path} is not executable."

def test_result_txt():
    file_path = "/home/user/result.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "4", f"Expected result.txt to contain '4', but found '{content}'."