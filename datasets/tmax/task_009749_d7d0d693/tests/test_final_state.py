# test_final_state.py

import os
from pathlib import Path

PROJECT_DIR = Path("/home/user/math_project")

def test_data_txt_recovered():
    data_file = PROJECT_DIR / "data.txt"
    assert data_file.exists(), "data.txt was not recovered."
    assert data_file.is_file(), "data.txt is not a file."

    content = data_file.read_text().strip().split()
    expected = ["4", "9", "16", "25", "36", "49", "64", "81", "100", "144"]
    assert content == expected, "data.txt does not contain the expected original data."

def test_result_txt_correct():
    result_file = PROJECT_DIR / "result.txt"
    assert result_file.exists(), "result.txt was not created. Did you run ./run_math.sh?"
    assert result_file.is_file(), "result.txt is not a file."

    content = result_file.read_text().strip()
    assert content == "Sum: 66.00", f"result.txt contains incorrect output: expected 'Sum: 66.00', got '{content}'"

def test_executable_exists():
    executable = PROJECT_DIR / "calculate"
    assert executable.exists(), "The 'calculate' executable was not built."
    assert os.access(executable, os.X_OK), "The 'calculate' file is not executable."