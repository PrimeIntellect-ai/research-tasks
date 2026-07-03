# test_final_state.py

import os
import pytest

def test_recovered_total_exists():
    path = "/home/user/recovered_total.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The tool may not have been run or failed to write the output."

def test_recovered_total_content():
    path = "/home/user/recovered_total.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_value = "1000048.64"
    assert content == expected_value, f"Expected {path} to contain '{expected_value}', but found '{content}'. Precision loss might not be completely fixed."

def test_cargo_toml_has_regex():
    path = "/home/user/fin_recover/Cargo.toml"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "regex" in content, f"Expected 'regex' dependency in {path}."

def test_main_rs_uses_f64():
    path = "/home/user/fin_recover/src/main.rs"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "f64" in content, f"Expected 'f64' to be used in {path} to fix precision loss."