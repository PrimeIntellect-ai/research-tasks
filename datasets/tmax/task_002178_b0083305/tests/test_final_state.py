# test_final_state.py

import os
import subprocess
import shutil
import filecmp
import pytest

def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def test_sanitizer_compiles_and_runs():
    project_dir = "/home/user/sanitizer"

    # Ensure the project exists
    assert os.path.exists(project_dir), f"Sanitizer project directory not found at {project_dir}"
    assert os.path.exists(os.path.join(project_dir, "Cargo.toml")), "Cargo.toml not found in sanitizer project"

    # Compile the project
    build_result = run_command("cargo build --release", cwd=project_dir)
    assert build_result.returncode == 0, f"Compilation failed:\n{build_result.stderr}"

    binary_path = os.path.join(project_dir, "target", "release", "sanitizer")
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Compiled binary is not executable at {binary_path}"

    # Setup output directories
    out_clean = "/tmp/out_clean"
    out_evil = "/tmp/out_evil"

    if os.path.exists(out_clean):
        shutil.rmtree(out_clean)
    if os.path.exists(out_evil):
        shutil.rmtree(out_evil)

    os.makedirs(out_clean, exist_ok=True)
    os.makedirs(out_evil, exist_ok=True)

    clean_corpus = "/app/verifier_corpus/clean"
    evil_corpus = "/app/verifier_corpus/evil"

    # Run against clean corpus
    run_clean = run_command(f"{binary_path} --input {clean_corpus} --output {out_clean}")
    assert run_clean.returncode == 0, f"Sanitizer failed on clean corpus:\n{run_clean.stderr}"

    # Run against evil corpus
    run_evil = run_command(f"{binary_path} --input {evil_corpus} --output {out_evil}")
    assert run_evil.returncode == 0, f"Sanitizer failed on evil corpus:\n{run_evil.stderr}"

    # Verify clean corpus preservation
    clean_original_files = []
    for root, _, files in os.walk(clean_corpus):
        for f in files:
            clean_original_files.append(os.path.relpath(os.path.join(root, f), clean_corpus))

    clean_copied_files = []
    for root, _, files in os.walk(out_clean):
        for f in files:
            clean_copied_files.append(os.path.relpath(os.path.join(root, f), out_clean))

    missing_clean = set(clean_original_files) - set(clean_copied_files)
    modified_clean = []

    for f in set(clean_original_files).intersection(set(clean_copied_files)):
        orig_path = os.path.join(clean_corpus, f)
        copy_path = os.path.join(out_clean, f)
        if not filecmp.cmp(orig_path, copy_path, shallow=False):
            modified_clean.append(f)

    assert not missing_clean, f"{len(missing_clean)} of {len(clean_original_files)} clean files were missing. Examples: {list(missing_clean)[:5]}"
    assert not modified_clean, f"{len(modified_clean)} of {len(clean_original_files)} clean files were modified. Examples: {modified_clean[:5]}"

    # Verify evil corpus rejection
    evil_copied_files = []
    for root, _, files in os.walk(out_evil):
        for f in files:
            evil_copied_files.append(os.path.relpath(os.path.join(root, f), out_evil))

    evil_original_files = []
    for root, _, files in os.walk(evil_corpus):
        for f in files:
            evil_original_files.append(os.path.relpath(os.path.join(root, f), evil_corpus))

    assert not evil_copied_files, f"{len(evil_copied_files)} of {len(evil_original_files)} evil files bypassed the filter. Examples: {evil_copied_files[:5]}"