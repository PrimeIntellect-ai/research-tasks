# test_final_state.py

import os

def test_regression_test_script_exists():
    path = "/home/user/regression_test.py"
    assert os.path.isfile(path), f"Missing file: {path}"

def test_output_npy_files_exist():
    # The task description doesn't explicitly specify the directory for the outputs,
    # but since the scripts run in the user's directory or the outputs are saved locally,
    # we check if they exist either in /home/user/ or current dir.
    # The setup script saves them to 'legacy_out.npy' and 'fast_out.npy' (relative to cwd).
    # Assuming they are created in /home/user or wherever the script was executed.
    # Let's check /home/user/ first, or just check that the text file is correct.
    # The prompt says they are saved as `legacy_out.npy` and `fast_out.npy`.
    pass # Not strictly necessary to enforce location if the txt file is correct, but let's check the txt file

def test_max_wasserstein_txt_content():
    path = "/home/user/max_wasserstein.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "0.003500", f"Expected '0.003500' in {path}, but got '{content}'"