# test_final_state.py
import os
import pytest

def test_parser_c_exists():
    path = "/home/user/parser.c"
    assert os.path.isfile(path), f"File {path} does not exist. You must create the C program."

def test_parser_executable_exists():
    path = "/home/user/parser"
    assert os.path.isfile(path), f"File {path} does not exist. You must compile the C program."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_process_sh_exists():
    path = "/home/user/process.sh"
    assert os.path.isfile(path), f"File {path} does not exist. You must create the bash script."

def test_processed_logins_csv_content():
    path = "/home/user/processed_logins.csv"
    assert os.path.isfile(path), f"File {path} does not exist. Your bash script must generate this file."

    expected_content = """1698062400,sysadmin
1698135330,admin!
1698135335,hacker
1698135365,test_user
1698135420,normal
1698195600,zoo"""

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {path} does not match the expected output. Expected:\n{expected_content}\nGot:\n{content}"