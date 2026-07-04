# test_final_state.py

import os
import pytest

def test_fit_model_script_exists_and_executable():
    script_path = "/home/user/fit_model.sh"
    assert os.path.isfile(script_path), f"File not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"File is not executable: {script_path}"

def test_best_fit_txt_content():
    best_fit_path = "/home/user/best_fit.txt"
    assert os.path.isfile(best_fit_path), f"File not found: {best_fit_path}"

    with open(best_fit_path, 'r') as f:
        content = f.read().strip()

    expected_content = "k=0.3, d=0.04"
    assert expected_content in content, f"Expected '{expected_content}' in {best_fit_path}, but found: '{content}'"