# test_final_state.py
import os
import re

def test_best_n_file():
    best_n_path = "/home/user/best_n.txt"
    assert os.path.isfile(best_n_path), f"File not found: {best_n_path}"

    with open(best_n_path, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Expected an integer in {best_n_path}, got '{content}'"
    best_n = int(content)
    assert best_n in [5, 10, 15, 20], f"Expected best_n to be one of [5, 10, 15, 20], got {best_n}"

def test_mse_file():
    mse_path = "/home/user/mse.txt"
    assert os.path.isfile(mse_path), f"File not found: {mse_path}"

    with open(mse_path, "r") as f:
        content = f.read().strip()

    # Check if it's a valid float rounded to 4 decimal places
    assert re.match(r"^\d+\.\d{4}$", content), f"Expected MSE to be a float rounded to exactly 4 decimal places, got '{content}'"

    try:
        mse = float(content)
    except ValueError:
        assert False, f"Could not parse '{content}' as a float"

    assert mse >= 0.0, "MSE cannot be negative"

def test_script_exists():
    script_path = "/home/user/process.py"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"