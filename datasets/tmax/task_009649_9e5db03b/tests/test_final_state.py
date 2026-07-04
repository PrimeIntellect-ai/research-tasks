# test_final_state.py

import os
import re
import pytest

def test_recovered_log():
    log_path = "/home/user/app/recovered.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    assert "[2023-10-27 10:01:05] Loss: 10.5" in content, "Recovered log is missing expected content."
    assert "[2023-10-27 10:05:25] Loss: 340.9" in content, "Recovered log is missing expected content."

def test_divergence_time():
    txt_path = "/home/user/app/divergence_time.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist."
    with open(txt_path, "r") as f:
        content = f.read().strip()

    assert content == "2023-10-27 10:04:20", f"Incorrect divergence time found: {content}"

def test_train_script_fixed():
    train_path = "/home/user/app/train.py"
    assert os.path.isfile(train_path), f"File {train_path} does not exist."
    with open(train_path, "r") as f:
        content = f.read()

    # Check if the bug was fixed
    assert re.search(r"x\s*=\s*x\s*-\s*learning_rate\s*\*\s*grad", content) or \
           re.search(r"x\s*-=\s*learning_rate\s*\*\s*grad", content), \
           "The weight update step in train.py was not fixed to subtract the gradient."

    # Check if the assertion was added
    assert "assert loss >= 0" in content.replace("0.0", "0"), "The assertion 'assert loss >= 0.0' is missing in train.py."

def test_success_txt():
    success_path = "/home/user/app/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} does not exist."
    with open(success_path, "r") as f:
        content = f.read().strip()

    assert "Final x: 3.000" in content, f"success.txt does not contain the expected converged value. Found: {content}"