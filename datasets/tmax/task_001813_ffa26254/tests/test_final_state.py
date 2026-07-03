# test_final_state.py
import os
import subprocess
import pytest

def get_filter_path():
    for ext in ["sh", "py", ""]:
        path = f"/home/user/doc_filter.{ext}" if ext else "/home/user/doc_filter"
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None

def test_filter_exists_and_executable():
    filter_path = get_filter_path()
    assert filter_path is not None, "Executable doc_filter script not found in /home/user/"

def test_adversarial_corpus():
    filter_path = get_filter_path()
    assert filter_path is not None, "Filter script missing, cannot test corpus."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_modified = []
    evil_bypassed = []

    for f in clean_files:
        result = subprocess.run([filter_path, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    for f in evil_files:
        result = subprocess.run([filter_path, f], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_compiled_docs():
    compiled_path = "/home/user/compiled_docs.md"
    assert os.path.isfile(compiled_path), f"Compiled docs file missing: {compiled_path}"

    with open(compiled_path, "r") as f:
        content = f.read().strip()

    assert content == "Draft 3 text", f"Compiled docs content is incorrect. Expected 'Draft 3 text', got: {content}"

def test_flock_used():
    flock_found = False

    history_files = ["/root/.bash_history", "/home/user/.bash_history"]
    for hf in history_files:
        if os.path.isfile(hf):
            with open(hf, "r", errors="ignore") as f:
                if "flock" in f.read():
                    flock_found = True
                    break

    if not flock_found:
        for root, dirs, files in os.walk("/home/user"):
            for file in files:
                if file.endswith(".sh") or file.endswith(".py"):
                    with open(os.path.join(root, file), "r", errors="ignore") as f:
                        if "flock" in f.read():
                            flock_found = True
                            break
            if flock_found:
                break

    assert flock_found, "flock command was not found in history or scripts. File locking requirement not met."