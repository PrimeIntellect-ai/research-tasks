# test_final_state.py

import os
import subprocess
import pytest

def test_bats_core_fixed():
    """Test that the vendored bats-core package is fixed and can run tests."""
    bats_bin = "/app/bats-core-1.11.0/bin/bats"
    test_file = "/app/corpus/clean/basic.bats"

    assert os.path.isfile(bats_bin), f"Bats executable {bats_bin} is missing."
    assert os.path.isfile(test_file), f"Test file {test_file} is missing."

    # Run the bats test
    result = subprocess.run([bats_bin, test_file], capture_output=True, text=True)

    assert result.returncode == 0, (
        f"bats-core is still broken. Running {bats_bin} {test_file} failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_bats_linter_adversarial_corpus():
    """Test the bats_linter.sh against the clean and evil corpora."""
    linter_script = "/home/user/bats_linter.sh"

    assert os.path.isfile(linter_script), f"Linter script {linter_script} is missing."

    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus_dir), f"Clean corpus directory {clean_corpus_dir} is missing."
    assert os.path.isdir(evil_corpus_dir), f"Evil corpus directory {evil_corpus_dir} is missing."

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]

    failed_clean = []
    failed_evil = []

    # Test clean files (must return 0)
    for f in clean_files:
        res = subprocess.run(["bash", linter_script, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    # Test evil files (must return != 0)
    for f in evil_files:
        res = subprocess.run(["bash", linter_script, f], capture_output=True)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(f))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    assert not error_messages, "Linter failed corpus checks:\n" + "\n".join(error_messages)