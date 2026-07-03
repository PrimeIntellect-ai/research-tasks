# test_final_state.py

import os
import stat

def test_evaluator_patched():
    filepath = "/home/user/math_release/src/evaluator.cpp"
    assert os.path.isfile(filepath), f"File missing: {filepath}"
    with open(filepath, "r") as f:
        content = f.read()
    assert 'if (token == "-") s.push(a - b);' in content, "The evaluator.cpp file does not contain the patched subtraction logic."
    assert 'b - a' not in content, "The buggy line was not removed from evaluator.cpp."

def test_makefile_exists():
    filepath = "/home/user/math_release/Makefile"
    assert os.path.isfile(filepath), f"Makefile missing: {filepath}"
    with open(filepath, "r") as f:
        content = f.read()
    assert "all" in content, "The Makefile does not define an 'all' target."
    assert "g++" in content or "c++" in content, "The Makefile does not seem to use a C++ compiler."
    assert "-std=c++17" in content, "The Makefile does not use the -std=c++17 flag."

def test_bin_directory_exists():
    dirpath = "/home/user/math_release/bin"
    assert os.path.isdir(dirpath), f"Directory missing: {dirpath}"

def test_executable_exists():
    filepath = "/home/user/math_release/bin/math_eval"
    assert os.path.isfile(filepath), f"Executable missing: {filepath}"
    st = os.stat(filepath)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {filepath} is not executable."

def test_deploy_results():
    filepath = "/home/user/math_release/deploy_results.log"
    assert os.path.isfile(filepath), f"Results log missing: {filepath}"
    with open(filepath, "r") as f:
        content = f.read().strip()

    expected_lines = ["8", "6", "10", "45"]
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"deploy_results.log content is incorrect. Expected {expected_lines}, but got {actual_lines}"