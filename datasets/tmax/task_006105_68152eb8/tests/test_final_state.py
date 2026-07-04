# test_final_state.py

import os

def test_train_features_output():
    train_file = "/home/user/train_features.txt"
    assert os.path.isfile(train_file), f"File {train_file} is missing. Did you run the compiled script?"

    with open(train_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected 8 lines in {train_file}, but got {len(lines)}."

    expected_train = [
        "1,1 2,-0.25",
        "2,1 3,1.75",
        "3,2 4,-2.25",
        "4,4 3,0.75",
        "5,1 5,0.25",
        "6,5 6,-1.25",
        "7,6 1,-0.25",
        "8,2 6,1.25"
    ]

    for i, (actual, expected) in enumerate(zip(lines, expected_train)):
        assert actual == expected, f"Line {i+1} in {train_file} is incorrect.\nExpected: {expected}\nGot: {actual}"

def test_test_features_output():
    test_file = "/home/user/test_features.txt"
    assert os.path.isfile(test_file), f"File {test_file} is missing. Did you run the compiled script?"

    with open(test_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {test_file}, but got {len(lines)}."

    expected_test = [
        "9,0 3,9.75",
        "10,0 5,11.75"
    ]

    for i, (actual, expected) in enumerate(zip(lines, expected_test)):
        assert actual == expected, f"Line {i+1} in {test_file} is incorrect.\nExpected: {expected}\nGot: {actual}"

def test_binary_exists():
    binary_file = "/home/user/prepare_data"
    assert os.path.isfile(binary_file), f"Compiled binary {binary_file} is missing. Did you recompile the script?"
    assert os.access(binary_file, os.X_OK), f"File {binary_file} is not executable."