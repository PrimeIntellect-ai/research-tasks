# test_final_state.py

import os
import pytest

def test_diagnosis_file_exists():
    diagnosis_path = "/home/user/diagnosis.txt"
    assert os.path.isfile(diagnosis_path), f"File {diagnosis_path} is missing. Did you create it?"

def test_diagnosis_file_content():
    diagnosis_path = "/home/user/diagnosis.txt"
    assert os.path.isfile(diagnosis_path), f"File {diagnosis_path} is missing."

    with open(diagnosis_path, 'r') as f:
        content = f.read().strip()

    expected = "EVT-8922=2023-10-25T18:45:00+28:00"

    assert content == expected, (
        f"Contents of {diagnosis_path} are incorrect.\n"
        f"Expected: '{expected}'\n"
        f"Found: '{content}'"
    )