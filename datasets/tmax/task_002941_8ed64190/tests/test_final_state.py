# test_final_state.py

import os
import subprocess

def test_mre_txt_content():
    path = "/home/user/mre.txt"
    assert os.path.isfile(path), f"{path} is missing. You must create an MRE file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_mre = "FX_TRADE,12345678.1234!"
    assert content == expected_mre, f"Content of {path} is incorrect. Expected '{expected_mre}', found '{content}'."

def test_parser_fixed_exists_and_executable():
    path = "/home/user/parser_fixed"
    assert os.path.isfile(path), f"{path} is missing. Did you compile the fixed C++ code?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_parser_fixed_output():
    parser_path = "/home/user/parser_fixed"
    transactions_path = "/home/user/transactions.txt"

    assert os.path.isfile(parser_path), f"Cannot test execution: {parser_path} is missing."
    assert os.path.isfile(transactions_path), f"Cannot test execution: {transactions_path} is missing."

    try:
        result = subprocess.run([parser_path, transactions_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Running {parser_path} {transactions_path} failed with return code {e.returncode}. Stderr: {e.stderr}"

    output = result.stdout.strip()
    expected_sum = "13345578.2233"

    assert output == expected_sum, f"The fixed parser output is incorrect. Expected '{expected_sum}', got '{output}'."

def test_final_sum_txt_content():
    path = "/home/user/final_sum.txt"
    assert os.path.isfile(path), f"{path} is missing. You must save the output to this file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_sum = "13345578.2233"
    assert content == expected_sum, f"Content of {path} is incorrect. Expected '{expected_sum}', found '{content}'."