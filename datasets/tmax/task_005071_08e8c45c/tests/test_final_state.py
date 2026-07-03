# test_final_state.py

import os
import pytest

def test_go_mod_exists_and_correct():
    go_mod_path = "/home/user/src/go.mod"
    assert os.path.isfile(go_mod_path), f"{go_mod_path} does not exist."

    with open(go_mod_path, "r") as f:
        content = f.read()

    assert "module mle/variance" in content, f"The go.mod file does not contain the correct module name 'mle/variance'."
    assert "gonum.org/v1/gonum" in content, "The go.mod file does not contain the gonum dependency."

def test_main_go_exists():
    main_go_path = "/home/user/src/main.go"
    assert os.path.isfile(main_go_path), f"{main_go_path} does not exist."

def test_eigen_txt_exists_and_correct():
    eigen_txt_path = "/home/user/output/eigen.txt"
    assert os.path.isfile(eigen_txt_path), f"{eigen_txt_path} does not exist."

    with open(eigen_txt_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "4.8690",
        "2.6508",
        "0.5482"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in eigen.txt, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected {expected}, got {actual}."