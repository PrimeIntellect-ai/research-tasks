# test_final_state.py
import os
import pytest

def test_output_file_exists_and_correct():
    output_path = "/home/user/legacy_app/output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the script and save the output?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["1.0", "20.0", "3.5"]
    assert lines == expected_lines, f"Contents of {output_path} do not match the expected equilibrium values. Got {lines}, expected {expected_lines}."

def test_app_py_still_exists_and_recursive():
    app_path = "/home/user/legacy_app/app.py"
    assert os.path.isfile(app_path), f"File {app_path} does not exist."

    with open(app_path, "r") as f:
        content = f.read()

    assert "def find_equilibrium" in content, "The find_equilibrium function must remain in app.py."
    assert "find_equilibrium(" in content.replace("def find_equilibrium", ""), "The function must remain recursive."