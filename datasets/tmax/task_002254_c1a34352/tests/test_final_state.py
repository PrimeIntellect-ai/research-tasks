# test_final_state.py
import os

def test_c_file_exists():
    assert os.path.isfile("/home/user/generate_feature.c"), "The C source file /home/user/generate_feature.c does not exist."

def test_executable_exists():
    assert os.path.isfile("/home/user/generate_feature"), "The executable /home/user/generate_feature does not exist. Did you compile the C program?"
    assert os.access("/home/user/generate_feature", os.X_OK), "/home/user/generate_feature is not executable."

def test_output_file_contents():
    output_file = "/home/user/ml_dataset_feature.txt"
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist. Did you run the program?"

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_content = "Energy: 147.227284"
    assert expected_content in content, f"Expected output '{expected_content}' not found in {output_file}. Found: '{content}'"