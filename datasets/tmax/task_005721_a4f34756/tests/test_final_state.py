# test_final_state.py

import os
import shutil

def test_h5dump_installed():
    """Verify that h5dump is installed."""
    assert shutil.which("h5dump") is not None, "h5dump is not installed. Did you install hdf5-tools?"

def test_fit_script_modified():
    """Verify that the fit.sh script was modified to lower the learning rate."""
    script_path = "/home/user/fit.sh"
    assert os.path.isfile(script_path), f"Script file is missing at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # The original script had lr = 0.5, which causes divergence.
    # It should have been changed to something smaller like 0.01.
    assert "lr = 0.5" not in content, "The learning rate in /home/user/fit.sh is still 0.5. It should be lowered."

def test_weight_file_exists_and_correct():
    """Verify that weight.txt exists and contains the correct weight."""
    weight_path = "/home/user/weight.txt"
    assert os.path.isfile(weight_path), f"Output file {weight_path} is missing. Did you run the script and save the output?"

    with open(weight_path, "r") as f:
        content = f.read().strip()

    assert content == "3.50", f"The weight in {weight_path} is '{content}', expected '3.50'. Make sure the script converged properly."