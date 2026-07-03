# test_final_state.py

import os
import re

def test_fixed_result_exists_and_correct():
    result_path = "/home/user/fixed_result.txt"
    assert os.path.isfile(result_path), f"Expected output file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "23.3993048391", f"The output in {result_path} is incorrect. Expected '23.3993048391', got '{content}'."

def test_go_code_modified_for_sorting():
    go_path = "/home/user/gc_calc.go"
    assert os.path.isfile(go_path), f"Go source file {go_path} is missing."

    with open(go_path, "r") as f:
        content = f.read()

    # Check if the "sort" package is imported
    assert re.search(r'"sort"', content), "The 'sort' package does not seem to be imported in the Go code, which is required for sorting the slice."

    # Check if the output formatting is correct
    assert '%.10f' in content, "The output format specifier '%.10f' is missing in the Go code."