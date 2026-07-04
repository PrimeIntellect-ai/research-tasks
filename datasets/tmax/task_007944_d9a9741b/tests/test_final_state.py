# test_final_state.py
import os

def test_extracted_files():
    extracted_dir = "/home/user/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    exp1_path = os.path.join(extracted_dir, "exp1.jsonl")
    exp2_path = os.path.join(extracted_dir, "exp2.jsonl")

    assert os.path.isfile(exp1_path), f"File {exp1_path} was not extracted."
    assert os.path.isfile(exp2_path), f"File {exp2_path} was not extracted."

    with open(exp1_path, "r") as f:
        exp1_content = f.read()
    assert exp1_content == '{"id": 1, "v": 150}\n{"id": 3, "v": 200}\n', f"Content of {exp1_path} is incorrect."

    with open(exp2_path, "r") as f:
        exp2_content = f.read()
    assert exp2_content == '{"id": 2, "v": 175}\n{"id": 4, "v": 220}\n', f"Content of {exp2_path} is incorrect."

def test_merged_csv():
    csv_path = "/home/user/merged.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    expected_csv = "id,v\n1,150\n2,175\n3,200\n4,220\n"
    expected_lines = [line.strip() for line in expected_csv.strip().split('\n')]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n')]

    assert actual_lines == expected_lines, f"Content of {csv_path} does not match the expected sorted CSV."

def test_extractor_cpp_exists():
    cpp_path = "/home/user/extractor.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."