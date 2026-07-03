# test_final_state.py
import os

def test_crack_cpp_exists():
    path = "/home/user/crack.cpp"
    assert os.path.isfile(path), f"File {path} is missing. You must create the C++ program to recover the password."

def test_findings_txt():
    path = "/home/user/findings.txt"
    assert os.path.isfile(path), f"File {path} is missing. You must create the report file."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, but found {len(lines)}."

    assert lines[0] == "admin", f"Line 1 of {path} is incorrect. Expected the recovered password."
    assert lines[1].upper() == "CWE-601", f"Line 2 of {path} is incorrect. Expected the CWE identifier (e.g., CWE-601)."