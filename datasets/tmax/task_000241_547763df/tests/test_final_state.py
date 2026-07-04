# test_final_state.py
import os

def test_recovered_logs_exists_and_valid():
    recovered_file = "/home/user/recovered_logs.txt"
    assert os.path.exists(recovered_file), f"Recovered log file {recovered_file} does not exist."

    with open(recovered_file, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    assert len(lines) == 10001, f"Expected 10001 lines in recovered logs, but found {len(lines)}."

def test_final_sum_correct():
    final_sum_file = "/home/user/final_sum.txt"
    assert os.path.exists(final_sum_file), f"Final sum file {final_sum_file} does not exist."

    with open(final_sum_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_sum = "100000099.68"
    assert content == expected_sum, f"Expected final sum to be exactly '{expected_sum}', but got '{content}'."