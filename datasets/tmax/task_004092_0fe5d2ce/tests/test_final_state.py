# test_final_state.py
import os
import subprocess
import glob

def test_script_exists_and_executable():
    script_path = "/home/user/filter_artifacts.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_clean_corpus_accepted():
    script_path = "/home/user/filter_artifacts.sh"
    clean_dir = "/app/clean"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    if not clean_files:
        clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([script_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0): {', '.join(failed_files)}"

def test_evil_corpus_rejected():
    script_path = "/home/user/filter_artifacts.sh"
    evil_dir = "/app/evil"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    if not evil_files:
        evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run([script_path, filepath], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed detection (exit code == 0): {', '.join(failed_files)}"