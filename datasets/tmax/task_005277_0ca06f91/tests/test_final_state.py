# test_final_state.py
import os

def test_result_file_exists():
    assert os.path.isfile('/home/user/result.txt'), "/home/user/result.txt does not exist."

def test_simulate_py_fixed_step_size():
    script_path = '/home/user/simulate.py'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    with open(script_path, 'r') as f:
        content = f.read()

    # Check if the formula has been corrected to use (tol / err)
    # Removing spaces to make the check robust
    content_no_spaces = content.replace(" ", "")
    assert "(tol/err)" in content_no_spaces or "tol/err" in content_no_spaces, "Step size adaptation formula not corrected (expected 'tol / err')."

def test_result_value():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"{result_path} does not exist."
    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {result_path} is not a valid float: '{content}'"

    assert 0.0001 <= val <= 0.0010, f"Result value {val} is not within the expected range [0.0001, 0.0010]."