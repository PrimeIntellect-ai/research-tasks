# test_final_state.py
import os
import subprocess
import pytest

def test_libparser_built():
    so_path = "/home/user/parser_project/libparser.so"
    assert os.path.isfile(so_path), f"Failed: {so_path} was not built."

def test_pin_txt_content():
    pin_path = "/home/user/pin.txt"
    assert os.path.isfile(pin_path), f"Failed: {pin_path} does not exist."
    with open(pin_path, "r") as f:
        content = f.read().strip()
    assert content == "8675309", f"Failed: {pin_path} contains '{content}', expected '8675309'."

def test_classifier_script_exists():
    script_path = "/home/user/classifier.py"
    assert os.path.isfile(script_path), f"Failed: {script_path} does not exist."

def test_classifier_clean_corpus():
    script_path = "/home/user/classifier.py"
    clean_dir = "/app/corpus/clean/"
    assert os.path.isdir(clean_dir), f"Failed: {clean_dir} does not exist."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert clean_files, "No files found in clean corpus."

    failures = []
    for fpath in clean_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if result.returncode != 0:
            failures.append(os.path.basename(fpath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files rejected (should be accepted): {', '.join(failures)}")

def test_classifier_evil_corpus():
    script_path = "/home/user/classifier.py"
    evil_dir = "/app/corpus/evil/"
    assert os.path.isdir(evil_dir), f"Failed: {evil_dir} does not exist."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert evil_files, "No files found in evil corpus."

    failures = []
    for fpath in evil_files:
        result = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if result.returncode != 1:
            failures.append(os.path.basename(fpath))

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed (should be rejected): {', '.join(failures)}")