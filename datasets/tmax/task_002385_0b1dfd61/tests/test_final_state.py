# test_final_state.py

import os
import subprocess

def test_recovered_records_exists_and_correct():
    path = "/home/user/recovered_records.csv"
    assert os.path.exists(path), f"File {path} does not exist. Did you recover it?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = """1,100,200
2,500,600
3,60000,50000
4,-10,20
5,70000,40000"""

    assert content == expected_content, "The recovered records do not match the expected original file contents."

def test_processor_compiled_and_correct():
    c_path = "/home/user/processor.c"
    bin_path = "/home/user/processor"

    assert os.path.exists(c_path), f"{c_path} is missing."
    assert os.path.exists(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

    # Test large numbers
    result = subprocess.run([bin_path, "60000", "50000"], capture_output=True, text=True)
    assert result.returncode == 0, "Processor binary crashed or returned non-zero."
    assert result.stdout.strip() == "3000000000", "Processor did not output the correct 64-bit multiplication result for large inputs."

    # Test negative numbers
    result_neg = subprocess.run([bin_path, "-10", "20"], capture_output=True, text=True)
    assert result_neg.returncode == 0, "Processor binary crashed on negative input."
    assert result_neg.stdout.strip() == "-1", "Processor did not output -1 for negative inputs."

def test_final_sum_correct():
    path = "/home/user/final_sum.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did daemon.py write the final sum?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "5800320000", f"Expected final sum to be 5800320000, but got {content}."