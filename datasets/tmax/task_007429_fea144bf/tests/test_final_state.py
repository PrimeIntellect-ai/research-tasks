# test_final_state.py
import os
import subprocess
import pytest

def test_mre_script_exists():
    """Check if the MRE script exists and is executable."""
    mre_path = "/home/user/mre.sh"
    assert os.path.exists(mre_path), f"{mre_path} does not exist."
    assert os.path.isfile(mre_path), f"{mre_path} is not a file."
    assert os.access(mre_path, os.X_OK), f"{mre_path} is not executable."

def test_answer_txt_content():
    """Check if the answer.txt contains the correct length."""
    answer_path = "/home/user/answer.txt"
    assert os.path.exists(answer_path), f"{answer_path} does not exist."
    with open(answer_path, "r") as f:
        content = f.read().strip()
    assert content == "21", f"Expected answer.txt to contain '21', but got '{content}'."

def test_solver_fixed_behavior():
    """Check if the solver.py script correctly handles floating point issues."""
    solver_path = "/home/user/service/solver.py"
    assert os.path.exists(solver_path), f"{solver_path} does not exist."

    # Run the solver with an input that would typically fail due to floating point precision
    # 0.3 - 0.1 - 0.1 - 0.1 usually doesn't equal exactly 0.0 in standard IEEE 754
    try:
        result = subprocess.run(
            ["python3", solver_path, "0.3"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("solver.py timed out, indicating an infinite loop/recursion is still present.")

    assert result.returncode == 0, f"solver.py failed with error: {result.stderr}"

    output = result.stdout.strip()
    assert output == "4", f"Expected solver.py 0.3 to output '4', but got '{output}'."

    # Test with 2.0
    try:
        result_2 = subprocess.run(
            ["python3", solver_path, "2.0"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("solver.py timed out for input 2.0.")

    assert result_2.returncode == 0, f"solver.py failed with error: {result_2.stderr}"
    output_2 = result_2.stdout.strip()
    assert output_2 == "21", f"Expected solver.py 2.0 to output '21', but got '{output_2}'."