# test_final_state.py

import os
import pytest

def test_result_txt_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. The program may not have run successfully."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "Average: 78", f"Expected content 'Average: 78', but got '{content}'"

def test_data_csv_unmodified():
    data_path = "/home/user/data_processor/data.csv"
    assert os.path.isfile(data_path), f"File {data_path} is missing."

    with open(data_path, "r") as f:
        content = f.read().strip()

    expected_content = "id,name,score\n1,Alice,45\n2,Bob,85\n3,Charlie,90\n4,Dave,60"

    # Normalize line endings for comparison
    content_normalized = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    expected_normalized = "\n".join(line.strip() for line in expected_content.splitlines() if line.strip())

    assert content_normalized == expected_normalized, "The data.csv file was modified, which violates the requirements."