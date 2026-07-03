# test_final_state.py

import os
import glob
import subprocess
import shutil

def test_archive_filter_script():
    script_path = "/home/user/archive_filter.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    clean_input = "/app/corpora/clean"
    evil_input = "/app/corpora/evil"
    clean_output = "/tmp/test_clean"
    evil_output = "/tmp/test_evil"
    password = "blue falcon seven"

    os.makedirs(clean_output, exist_ok=True)
    os.makedirs(evil_output, exist_ok=True)

    # Run on clean corpus
    res_clean = subprocess.run([
        "python3", script_path,
        "--input", clean_input,
        "--output", clean_output,
        "--password", password
    ], capture_output=True, text=True)

    assert res_clean.returncode == 0, f"Script failed on clean corpus:\n{res_clean.stderr}"

    # Run on evil corpus
    res_evil = subprocess.run([
        "python3", script_path,
        "--input", evil_input,
        "--output", evil_output,
        "--password", password
    ], capture_output=True, text=True)

    assert res_evil.returncode == 0, f"Script failed on evil corpus:\n{res_evil.stderr}"

    # Verify clean corpus
    clean_input_files = [os.path.basename(f) for f in glob.glob(os.path.join(clean_input, "*.tar"))]
    clean_output_files = [os.path.basename(f) for f in glob.glob(os.path.join(clean_output, "*.tar"))]

    missing_clean = set(clean_input_files) - set(clean_output_files)
    assert not missing_clean, f"{len(missing_clean)} of {len(clean_input_files)} clean files were not preserved: {missing_clean}"

    # Verify evil corpus
    evil_input_files = [os.path.basename(f) for f in glob.glob(os.path.join(evil_input, "*.tar"))]
    evil_output_files = [os.path.basename(f) for f in glob.glob(os.path.join(evil_output, "*.tar"))]

    assert not evil_output_files, f"{len(evil_output_files)} of {len(evil_input_files)} evil files bypassed: {evil_output_files}"

    # Verify hardlinks for clean
    for f in clean_output_files:
        src = os.path.join(clean_input, f)
        dst = os.path.join(clean_output, f)
        assert os.stat(src).st_ino == os.stat(dst).st_ino, f"File {f} is not a hardlink."