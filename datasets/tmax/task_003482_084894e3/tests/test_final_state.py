# test_final_state.py

import os
import stat

def test_extractor_c_exists():
    path = '/home/user/extractor.c'
    assert os.path.isfile(path), f"The C source file {path} was not found."

def test_extractor_executable_exists():
    path = '/home/user/extractor'
    assert os.path.isfile(path), f"The compiled executable {path} was not found."

    # Check if it's executable
    st = os.stat(path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"The file {path} is not executable."

def test_unique_product_codes_csv():
    path = '/home/user/unique_product_codes.csv'
    assert os.path.isfile(path), f"The output file {path} was not found."

    expected_codes = [
        "abc-1234",
        "def-5678",
        "lmn-0000",
        "qwe-1111",
        "xyz-9999",
        "zzz-9999"
    ]

    with open(path, 'r') as f:
        content = f.read().strip().splitlines()

    assert content == expected_codes, (
        f"The content of {path} does not match the expected output.\n"
        f"Expected: {expected_codes}\n"
        f"Got:      {content}"
    )