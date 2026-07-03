# test_final_state.py

import os

def test_shortest_path_result():
    path_file = "/home/user/audit/shortest_path.txt"
    assert os.path.isfile(path_file), f"The file {path_file} does not exist. Did you run your Rust program?"

    with open(path_file, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected shortest path length to be '3', but got '{content}'."