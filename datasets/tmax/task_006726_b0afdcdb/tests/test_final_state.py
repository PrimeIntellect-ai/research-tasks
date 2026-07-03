# test_final_state.py
import os

def test_matches_output():
    path = "/home/user/matches.txt"
    assert os.path.isfile(path), f"File {path} is missing. The C program must write results to this file."

    with open(path, "r") as f:
        content = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    expected = [
        "Alice cites Bob",
        "Alice cites Dave",
        "Charlie cites Bob",
        "Charlie cites Frank",
        "Eve cites Frank"
    ]

    assert content == expected, f"Content of {path} is incorrect.\nExpected:\n{expected}\nGot:\n{content}"

def test_executable_exists():
    path = "/home/user/pattern_match_exe"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile your C program to this path?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_source_files_exist():
    c_path = "/home/user/pattern_match.c"
    sh_path = "/home/user/etl.sh"

    assert os.path.isfile(c_path), f"C source file {c_path} is missing."
    assert os.path.isfile(sh_path), f"Shell script {sh_path} is missing."