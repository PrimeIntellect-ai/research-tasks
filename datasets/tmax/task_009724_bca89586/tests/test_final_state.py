# test_final_state.py

import os
import subprocess
import pytest

def test_fixed_calc_executable_exists():
    executable_path = "/home/user/fixed_calc"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_solution_txt_content():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"Solution file {solution_path} does not exist."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content == "Risk Score: 15", f"Expected 'Risk Score: 15' in {solution_path}, but got '{content}'."

def test_fixed_calc_execution():
    executable_path = "/home/user/fixed_calc"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."

    try:
        result = subprocess.run(
            [executable_path, "9942"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert output == "Risk Score: 15", f"Expected executable to output 'Risk Score: 15', but got '{output}'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {executable_path} failed. It may still be crashing. Error: {e.stderr}")