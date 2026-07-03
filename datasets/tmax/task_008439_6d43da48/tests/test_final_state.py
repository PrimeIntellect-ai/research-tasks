# test_final_state.py

import os
import stat

def test_script_exists_and_executable():
    """Test that /home/user/run_optimization.sh exists and is executable."""
    script_path = "/home/user/run_optimization.sh"

    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_best_fit_output():
    """Test that /home/user/best_fit.txt contains the correct optimal parameters and MSE."""
    output_path = "/home/user/best_fit.txt"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected = "11.7,1.9,0.1234"
    assert content == expected, f"Expected '{expected}' in {output_path}, but got '{content}'."