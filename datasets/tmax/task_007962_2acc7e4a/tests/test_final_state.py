# test_final_state.py

import os
import glob

def test_result_txt_exists_and_correct():
    result_path = "/home/user/legacy_app/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. The script mre.py was either not run or failed to create it."

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected = "SUCCESS_DECODED_ANOMALY_99X"
    assert content == expected, f"Expected '{expected}' in result.txt, but got '{content}'."

def test_mre_py_exists():
    mre_path = "/home/user/legacy_app/mre.py"
    assert os.path.isfile(mre_path), f"File {mre_path} does not exist. You must create the minimal reproducible example script."

def test_extension_compiled():
    # Check if the .so file was successfully built in the directory
    so_files = glob.glob("/home/user/legacy_app/processor*.so")
    assert len(so_files) > 0, "The processor C-extension (.so file) was not found. Ensure setup.py compiles it successfully."