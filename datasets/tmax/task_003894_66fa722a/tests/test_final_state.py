# test_final_state.py
import os

def test_parser_c_exists():
    path = "/home/user/parser.c"
    assert os.path.exists(path), f"File {path} does not exist. You must write your C code to this file."
    assert os.path.isfile(path), f"Path {path} is not a valid file."

def test_extracted_text_exists():
    path = "/home/user/extracted_text.txt"
    assert os.path.exists(path), f"File {path} does not exist. Your C program must create this file."
    assert os.path.isfile(path), f"Path {path} is not a valid file."

def test_extracted_text_content():
    path = "/home/user/extracted_text.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_content = "Project_Start\nModule_Active\nConfig_Loaded\n"

    assert content == expected_content, (
        f"The content of {path} does not match the expected output.\n"
        f"Expected:\n{repr(expected_content)}\n"
        f"Got:\n{repr(content)}"
    )