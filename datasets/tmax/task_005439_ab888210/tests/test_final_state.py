# test_final_state.py

import os
import pytest

def test_cleaned_data_exists_and_correct():
    file_path = "/home/user/cleaned_data.csv"

    # Check if file exists
    assert os.path.exists(file_path), f"The output file {file_path} is missing. Did the Rust program run and save the file?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    # Expected content based on the derivation
    expected_content = (
        "temp,pressure,humidity,vibration\n"
        "10.0,101.2,45.0,0.5\n"
        "12.0,101.5,41.0,0.6\n"
        "14.0,101.1,37.0,0.5\n"
        "16.0,100.9,33.0,0.4\n"
        "18.0,100.8,29.0,0.5\n"
        "20.0,100.5,25.0,0.6"
    )

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {file_path} does not match the expected final state.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}\n"
        "Ensure the missing value is correctly imputed and all numbers are formatted to one decimal place."
    )