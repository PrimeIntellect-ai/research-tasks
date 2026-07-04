# test_final_state.py

import os
import stat
import pytest

def test_etl_script_exists_and_executable():
    path = "/home/user/etl.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_clean_data_created():
    train_path = "/home/user/clean_train.tsv"
    test_path = "/home/user/clean_test.tsv"

    assert os.path.isfile(train_path), f"File {train_path} is missing."
    assert os.path.isfile(test_path), f"File {test_path} is missing."

    with open(train_path, 'r') as f:
        train_lines = [line.strip() for line in f if line.strip()]

    with open(test_path, 'r') as f:
        test_lines = [line.strip() for line in f if line.strip()]

    assert len(train_lines) == 3, f"Expected 3 lines in {train_path}, found {len(train_lines)}."
    assert len(test_lines) == 3, f"Expected 3 lines in {test_path}, found {len(test_lines)}."

    expected_train_ids = {"1", "5", "9"}
    actual_train_ids = {line.split('\t')[0] for line in train_lines}
    assert actual_train_ids == expected_train_ids, f"Expected train IDs {expected_train_ids}, got {actual_train_ids}."

    expected_test_ids = {"3", "6", "8"}
    actual_test_ids = {line.split('\t')[0] for line in test_lines}
    assert actual_test_ids == expected_test_ids, f"Expected test IDs {expected_test_ids}, got {actual_test_ids}."

def test_reduce_script_exists_and_executable():
    path = "/home/user/reduce.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_tune_script_exists_and_executable():
    path = "/home/user/tune.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_best_params_output():
    path = "/home/user/best_params.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did tune.sh run and create it?"

    with open(path, 'r') as f:
        content = f.read().strip()

    # The expected score is derived from the parameters and evaluate.py logic
    expected = "K=6,T=0.5,Score=60.00"

    # We allow some flexibility if the student formatted the score slightly differently, 
    # but the instructions said "exactly one line in this format: K=<best_K>,T=<best_T>,Score=<highest_score>"
    # and evaluate.py prints 2 decimal places.
    assert expected in content or content == expected.replace("60.00", "60.0"), \
        f"Contents of {path} do not match the expected best parameters. Got: '{content}'"