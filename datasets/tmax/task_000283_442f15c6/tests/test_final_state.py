# test_final_state.py
import os
import subprocess
import pytest

def test_waf_filter_executable_exists():
    binary_path = "/app/bin/waf_filter"
    assert os.path.isfile(binary_path), f"The Go binary is missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"The file at {binary_path} is not executable"

def test_waf_filter_adversarial_corpus():
    binary_path = "/app/bin/waf_filter"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_modified = []
    for cf in clean_files:
        try:
            result = subprocess.run([binary_path, cf], capture_output=True, text=True, timeout=5)
            if result.returncode != 0 or "CLEAN" not in result.stdout:
                clean_modified.append(os.path.basename(cf))
        except Exception as e:
            clean_modified.append(f"{os.path.basename(cf)} (error: {e})")

    evil_bypassed = []
    for ef in evil_files:
        try:
            result = subprocess.run([binary_path, ef], capture_output=True, text=True, timeout=5)
            if result.returncode != 1 or "EVIL" not in result.stdout:
                evil_bypassed.append(os.path.basename(ef))
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(ef)} (error: {e})")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus validation failed:\n" + "\n".join(errors)