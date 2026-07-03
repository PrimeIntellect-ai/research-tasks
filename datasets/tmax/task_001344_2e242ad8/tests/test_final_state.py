# test_final_state.py
import os
import subprocess
import pytest

def test_filter_binary_exists():
    binary_path = "/home/user/filter"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_adversarial_corpus_clean():
    binary_path = "/home/user/filter"
    clean_dir = "/corpus/clean/"
    assert os.path.exists(clean_dir), f"Clean corpus directory {clean_dir} does not exist."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No files found in clean corpus."

    modified = []
    for filepath in clean_files:
        try:
            result = subprocess.run([binary_path, filepath], capture_output=True, text=True, timeout=1)
            output = result.stdout.strip()
            if output != "CLEAN":
                modified.append(os.path.basename(filepath))
        except Exception as e:
            modified.append(os.path.basename(filepath))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified (expected CLEAN). Offending files: {modified[:10]}")

def test_adversarial_corpus_evil():
    binary_path = "/home/user/filter"
    evil_dir = "/corpus/evil/"
    assert os.path.exists(evil_dir), f"Evil corpus directory {evil_dir} does not exist."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed = []
    for filepath in evil_files:
        try:
            result = subprocess.run([binary_path, filepath], capture_output=True, text=True, timeout=1)
            output = result.stdout.strip()
            if output != "EVIL":
                bypassed.append(os.path.basename(filepath))
        except Exception as e:
            # If it crashes or fails to run, we might consider it bypassed or just failed, but EVIL is expected.
            bypassed.append(os.path.basename(filepath))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed (expected EVIL). Offending files: {bypassed[:10]}")