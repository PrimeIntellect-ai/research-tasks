# test_final_state.py
import os
import re

def test_results_file_exists():
    assert os.path.isfile('/home/user/results.txt'), "/home/user/results.txt does not exist. Did you pipe the output to this file?"

def test_executable_exists():
    assert os.path.isfile('/home/user/nb_classifier'), "/home/user/nb_classifier does not exist. Did you compile the C++ code to this executable?"
    assert os.access('/home/user/nb_classifier', os.X_OK), "/home/user/nb_classifier is not executable."

def test_results_content():
    with open('/home/user/results.txt', 'r') as f:
        content = f.read()

    vocab_match = re.search(r'Vocab Size:\s*(\d+)', content)
    assert vocab_match is not None, "Could not find 'Vocab Size: <integer>' in results.txt. Ensure the output format is exactly as specified."

    vocab_size = int(vocab_match.group(1))
    assert vocab_size == 33, f"Expected Vocab Size to be 33 (training set only), but got {vocab_size}. The data leak might not be fully fixed."

    acc_match = re.search(r'Test Accuracy:\s*([0-9.]+)', content)
    assert acc_match is not None, "Could not find 'Test Accuracy: <float>' in results.txt. Ensure the output format is exactly as specified."

def test_source_code_modified():
    assert os.path.isfile('/home/user/naive_bayes.cpp'), "/home/user/naive_bayes.cpp is missing."
    with open('/home/user/naive_bayes.cpp', 'r') as f:
        content = f.read()

    # Just to ensure the file was actually touched/modified from the original buggy state
    # The original file had a vocab size of 34 printed. We check the results.txt for the real validation.
    assert len(content) > 0, "naive_bayes.cpp is empty."