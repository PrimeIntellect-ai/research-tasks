# test_final_state.py
import os
import glob
import subprocess

def test_helper_compiled():
    so_path = "/home/user/legacy_pipeline/helper.so"
    assert os.path.isfile(so_path), f"Expected compiled shared object at {so_path} but it was not found. Did you fix the build script and run it?"

def test_validator_clean_corpus():
    validator_path = "/home/user/legacy_pipeline/validator.py"
    clean_dir = "/home/user/corpora/clean"

    assert os.path.isfile(validator_path), f"Validator script {validator_path} missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        result = subprocess.run(["python3", validator_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        assert False, f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0). Offending files: {', '.join(failed_files[:10])}{'...' if len(failed_files) > 10 else ''}"

def test_validator_evil_corpus():
    validator_path = "/home/user/legacy_pipeline/validator.py"
    evil_dir = "/home/user/corpora/evil"

    assert os.path.isfile(validator_path), f"Validator script {validator_path} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for f in evil_files:
        result = subprocess.run(["python3", validator_path, f], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        assert False, f"{len(failed_files)} of {len(evil_files)} evil files bypassed validation (exit code == 0). Offending files: {', '.join(failed_files[:10])}{'...' if len(failed_files) > 10 else ''}"