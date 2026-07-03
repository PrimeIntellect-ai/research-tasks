# test_final_state.py
import os

def test_final_accuracy_file():
    path = '/home/user/final_accuracy.txt'
    assert os.path.exists(path), f"{path} is missing. Did you run the cross-validation script?"
    with open(path, 'r') as f:
        content = f.read().strip()

    # Since the data is perfectly separable once NaN is ignored, the accuracy should be 1.00
    assert content == "1.00", f"Expected final accuracy to be exactly '1.00', but got '{content}'"

def test_classifier_c_modified():
    path = '/home/user/classifier.c'
    assert os.path.exists(path), f"{path} is missing."
    with open(path, 'r') as f:
        content = f.read()

    # The instructions explicitly mention skipping rows where the feature is "NaN"
    assert "NaN" in content, "classifier.c does not appear to contain logic checking for the string 'NaN'."

def test_compiled_classifier_exists():
    path = '/home/user/classifier'
    assert os.path.exists(path), f"Compiled executable {path} is missing."
    assert os.access(path, os.X_OK), f"{path} is not executable. Did you compile it correctly?"

def test_run_cv_script_exists():
    path = '/home/user/run_cv.sh'
    assert os.path.exists(path), f"{path} is missing."