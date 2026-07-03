# test_final_state.py
import os

def test_eigen_stats_output():
    file_path = "/home/user/eigen_stats.txt"

    assert os.path.isfile(file_path), f"File {file_path} does not exist. The script must create this file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "Mean: 2.6667\nStdDev: 0.5774"

    assert content == expected_content, (
        f"Content of {file_path} is incorrect.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )