# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/loc_cleaner.c"
    assert os.path.exists(path), f"The C source file {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."

def test_executable_exists():
    path = "/home/user/loc_cleaner"
    assert os.path.exists(path), f"The executable {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_clean_locales_content():
    path = "/home/user/clean_locales.ini"
    assert os.path.exists(path), f"The output file {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."

    expected_content = (
        "ERR_FILE_MISSING=Error: File not found\n"
        "MAIN_MENU_OPTIONS=Options\n"
        "MAIN_MENU_PLAY=Start Game\n"
        "TRICKY_VAL=This value has : a colon\n"
        "VALID_EMPTY=\n"
    )

    with open(path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"The content of {path} is incorrect. Expected:\n{expected_content}\nGot:\n{actual_content}"