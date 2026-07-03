# test_final_state.py

import os

def test_weather_summary_exists_and_content():
    file_path = "/home/user/weather_summary.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did the C program run and generate the output?"

    expected_content = (
        "Total Missing Hours Filled: 18\n"
        "Max Levenshtein Distance: 22 (between hour 4 and hour 5)\n"
        "Average Levenshtein Distance: 3.17"
    )

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} does not match the expected summary. Got:\n{content}"