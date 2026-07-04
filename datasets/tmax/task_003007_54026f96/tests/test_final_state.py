# test_final_state.py
import os
import glob
import subprocess

def test_fast_validator_exists_and_executable():
    binary_path = "/home/user/fast_validator"
    go_path = "/home/user/fast_validator.go"

    # If the binary doesn't exist but the source does, try to compile it
    if not os.path.exists(binary_path) and os.path.exists(go_path):
        subprocess.run(["go", "build", "-o", binary_path, go_path], cwd="/home/user", capture_output=True)

    assert os.path.exists(binary_path), f"Missing compiled binary at {binary_path}"
    assert os.path.isfile(binary_path), f"{binary_path} is not a file"
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable"

def test_fast_validator_clean_corpus():
    binary_path = "/home/user/fast_validator"
    clean_dir = "/eval/corpus/clean"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run([binary_path, fpath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "VALID":
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        msg = f"{len(failed_files)} of {len(clean_files)} clean modified (rejected or invalid output). Offending files: {', '.join(failed_files[:10])}"
        if len(failed_files) > 10:
            msg += "..."
        assert False, msg

def test_fast_validator_evil_corpus():
    binary_path = "/home/user/fast_validator"
    evil_dir = "/eval/corpus/evil"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    failed_files = []
    for fpath in evil_files:
        result = subprocess.run([binary_path, fpath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "INVALID":
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        msg = f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted or invalid output). Offending files: {', '.join(failed_files[:10])}"
        if len(failed_files) > 10:
            msg += "..."
        assert False, msg