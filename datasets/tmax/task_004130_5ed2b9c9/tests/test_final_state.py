# test_final_state.py
import os

def test_shortest_path_result():
    output_file = "/home/user/shortest_path.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    expected_content = "Latency: 40\nPath: S,A,C,T"

    with open(output_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Content of {output_file} is incorrect. Expected:\n{expected_content}\nGot:\n{actual_content}"