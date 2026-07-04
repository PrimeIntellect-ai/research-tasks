# test_final_state.py

import os

def test_bottleneck_analysis_result():
    result_file = "/home/user/bottleneck_analysis.txt"

    assert os.path.exists(result_file), f"The file {result_file} was not created."
    assert os.path.isfile(result_file), f"{result_file} is not a regular file."

    with open(result_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "orders", (
        f"Incorrect bottleneck table identified. "
        f"Expected 'orders', but found '{content}' in {result_file}."
    )