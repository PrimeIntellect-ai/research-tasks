# test_final_state.py
import os

def test_tvd_result_exists():
    result_file = "/home/user/tvd_result.txt"
    assert os.path.exists(result_file), f"Failed: {result_file} not found. Ensure your Go program writes to this file."

def test_tvd_result_value():
    result_file = "/home/user/tvd_result.txt"
    assert os.path.exists(result_file), f"Failed: {result_file} not found."

    with open(result_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Failed: The content of {result_file} is not a valid float: '{content}'"

    assert 0.0480 <= val <= 0.0520, f"Failed: TVD {val} is not within the acceptable range (0.0480 - 0.0520). Check your random walk simulation logic and TVD calculation."

def test_go_source_exists():
    source_file = "/home/user/mc_fit.go"
    assert os.path.exists(source_file), f"Failed: {source_file} not found. You must write your Go program to this file."