# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_build_script_fixed():
    build_script = '/app/sqlite-src/build.sh'
    assert os.path.isfile(build_script), f"{build_script} is missing."
    with open(build_script, 'r') as f:
        content = f.read()
    assert '-DSQLITE_OMIT_CTE' not in content, "The -DSQLITE_OMIT_CTE flag was not removed from /app/sqlite-src/build.sh"

def test_checker_exists_and_executable():
    checker_path = '/home/user/checker'
    assert os.path.isfile(checker_path), f"Checker executable not found at {checker_path}"
    assert os.access(checker_path, os.X_OK), f"Checker at {checker_path} is not executable"

def test_adversarial_corpus():
    checker_path = '/home/user/checker'
    clean_dir = '/home/user/corpora/clean/'
    evil_dir = '/home/user/corpora/evil/'

    clean_files = glob.glob(os.path.join(clean_dir, '*.db'))
    evil_files = glob.glob(os.path.join(evil_dir, '*.db'))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run([checker_path, cf], capture_output=True, text=True)
        if res.returncode != 0 or res.stdout.strip() != 'CLEAN':
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run([checker_path, ef], capture_output=True, text=True)
        if res.returncode != 1 or res.stdout.strip() != 'EVIL':
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (failed to accept): {', '.join(failed_clean)}")

    assert not failed_clean and not failed_evil, "\n".join(error_msgs)