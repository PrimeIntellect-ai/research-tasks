# test_final_state.py

import os
import pytest

def test_shortest_path_output():
    output_file = "/home/user/shortest_path.txt"

    assert os.path.exists(output_file), f"The file {output_file} does not exist."
    assert os.path.isfile(output_file), f"The path {output_file} is not a file."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected the output file to contain exactly '3', but found '{content}'."