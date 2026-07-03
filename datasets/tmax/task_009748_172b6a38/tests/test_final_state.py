# test_final_state.py
import os

def test_result_txt_content():
    result_file = "/home/user/result.txt"
    assert os.path.exists(result_file), f"The output file {result_file} does not exist. Did you run the program and redirect the output?"

    with open(result_file, "r") as f:
        content = f.read().strip()

    expected = "Anomaly Mean: 16.67"
    assert content == expected, f"Expected '{expected}' in {result_file}, but found '{content}'. Ensure you correctly recovered the key and skipped the corrupted records."