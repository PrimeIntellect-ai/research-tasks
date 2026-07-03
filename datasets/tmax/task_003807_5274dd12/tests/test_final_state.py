# test_final_state.py

import os
import subprocess
import glob
import time
import pytest

def test_pdat_filter_exists():
    binary_path = "/home/user/pdat_filter"
    assert os.path.isfile(binary_path), f"Expected binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_clean_corpus():
    clean_dir = "/tests/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    assert clean_files, f"No clean files found in {clean_dir}"

    failed = []
    for f in clean_files:
        res = subprocess.run(["/home/user/pdat_filter", f], capture_output=True)
        if res.returncode != 0:
            failed.append(os.path.basename(f))

    assert not failed, f"{len(failed)} of {len(clean_files)} clean files rejected (should exit 0): {failed}"

def test_evil_corpus():
    evil_dir = "/tests/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    assert evil_files, f"No evil files found in {evil_dir}"

    failed = []
    for f in evil_files:
        res = subprocess.run(["/home/user/pdat_filter", f], capture_output=True)
        if res.returncode == 0:
            failed.append(os.path.basename(f))

    assert not failed, f"{len(failed)} of {len(evil_files)} evil files bypassed (should exit 1): {failed}"

def test_watch_script():
    watch_script = "/home/user/watch.sh"
    assert os.path.isfile(watch_script), f"Expected script {watch_script} does not exist."
    assert os.access(watch_script, os.X_OK), f"The script {watch_script} is not executable."

    # Start watch.sh in the background
    proc = subprocess.Popen([watch_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        # Give inotifywait time to initialize
        time.sleep(1)

        # Copy a clean file to incoming
        clean_files = glob.glob("/tests/corpora/clean/*")
        if clean_files:
            subprocess.run(["cp", clean_files[0], "/home/user/incoming/test_clean.pdat"], check=True)

        # Copy an evil file to incoming
        evil_files = glob.glob("/tests/corpora/evil/*")
        if evil_files:
            subprocess.run(["cp", evil_files[0], "/home/user/incoming/test_evil.pdat"], check=True)

        # Wait for the script to process the files
        time.sleep(2)

        # Verify file movements
        assert os.path.exists("/home/user/accepted/test_clean.pdat"), "Clean file was not moved to /home/user/accepted/"
        assert os.path.exists("/home/user/rejected/test_evil.pdat"), "Evil file was not moved to /home/user/rejected/"

        # Verify log contents
        log_path = "/home/user/process.log"
        assert os.path.exists(log_path), f"Log file {log_path} was not created."

        with open(log_path, "r") as f:
            log_content = f.read()

        assert "test_clean.pdat: ACCEPTED" in log_content, "Clean file processing was not logged correctly."
        assert "test_evil.pdat: REJECTED" in log_content, "Evil file processing was not logged correctly."

    finally:
        proc.terminate()
        proc.wait(timeout=2)