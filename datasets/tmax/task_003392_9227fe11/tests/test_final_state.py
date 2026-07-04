# test_final_state.py

import os
import subprocess
import pytest

def test_constant_extracted():
    constant_file = "/home/user/constant.txt"
    assert os.path.isfile(constant_file), f"File {constant_file} does not exist."

    with open(constant_file, "r") as f:
        content = f.read().strip()

    assert content == "314159", f"Expected constant '314159', but got '{content}'."

def test_math_pipeline_tests_pass():
    pipeline_dir = "/home/user/math_pipeline"
    assert os.path.isdir(pipeline_dir), f"Directory {pipeline_dir} does not exist."

    result = subprocess.run(
        ["pytest"],
        cwd=pipeline_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest in {pipeline_dir} failed. Output:\n{result.stdout}\n{result.stderr}"

def test_sanitizer_adversarial_corpus():
    sanitizer_script = "/home/user/math_pipeline/sanitizer.py"
    assert os.path.isfile(sanitizer_script), f"Sanitizer script {sanitizer_script} does not exist."

    clean_corpus_dir = "/app/corpora/clean"
    evil_corpus_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_corpus_dir), f"Clean corpus directory {clean_corpus_dir} does not exist."
    assert os.path.isdir(evil_corpus_dir), f"Evil corpus directory {evil_corpus_dir} does not exist."

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if f.endswith('.wav')]
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if f.endswith('.wav')]

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    failed_clean = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", sanitizer_script, clean_file], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(clean_file))

    failed_evil = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", sanitizer_script, evil_file], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(evil_file))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    assert not errors, "Sanitizer failed on corpus:\n" + "\n".join(errors)