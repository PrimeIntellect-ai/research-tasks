# test_final_state.py

import os
import re
import pytest

def test_result_txt_exists_and_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"{path} is missing. Did you run your main.go program and save the output?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "99.99450", f"Expected result.txt to exactly contain '99.99450', found '{content}'"

def test_fuzz_test_exists():
    path = "/home/user/uptime-app/calc_test.go"
    assert os.path.isfile(path), f"{path} is missing. You need to create the fuzz test file."
    with open(path, "r") as f:
        content = f.read()
    assert "func FuzzParseMetric(f *testing.F)" in content, "calc_test.go is missing the fuzzer function signature: func FuzzParseMetric(f *testing.F)"

def test_calculate_average_signature():
    path = "/home/user/uptime-app/calc.go"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()

    # Check that CalculateAverage now returns float64
    match = re.search(r"func\s+CalculateAverage\s*\([^)]*\[\]float32\)\s+float64", content)
    assert match is not None, "CalculateAverage signature in calc.go is not updated to return float64"

def test_main_go_exists():
    path = "/home/user/uptime-app/main.go"
    assert os.path.isfile(path), f"{path} is missing. You need to write the main application logic here."