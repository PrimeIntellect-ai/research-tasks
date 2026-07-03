# test_final_state.py
import os
import re

def test_result_file_exists():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Expected result file {result_path} does not exist. Did you run the program and redirect stdout?"

def test_result_file_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), "Result file missing."

    with open(result_path, "r") as f:
        content = f.read()

    assert re.search(r"TCP packets:\s*150", content), "TCP packets count is incorrect or missing in result.txt. Expected 150."
    assert re.search(r"UDP packets:\s*85", content), "UDP packets count is incorrect or missing in result.txt. Expected 85."
    assert re.search(r"Total processed:\s*235", content), "Total processed count is incorrect or missing in result.txt. Expected 235."