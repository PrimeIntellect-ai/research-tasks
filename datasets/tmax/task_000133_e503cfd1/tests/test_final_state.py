# test_final_state.py

import os
import subprocess
import tempfile
import shutil

def test_classifier_exists_and_executable():
    executable = "/home/user/classifier"
    assert os.path.isfile(executable), f"Executable not found at {executable}"
    assert os.access(executable, os.X_OK), f"File at {executable} is not executable"

def test_adversarial_corpus():
    executable = "/home/user/classifier"
    target_sequence = "ATGCGTACGTTAGCTAGCTAGCTA"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus dir missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus dir missing: {evil_dir}"

    clean_files = set(f for f in os.listdir(clean_dir) if f.endswith('.txt'))
    evil_files = set(f for f in os.listdir(evil_dir) if f.endswith('.txt'))

    assert len(clean_files) > 0, "No .txt files found in clean corpus."
    assert len(evil_files) > 0, "No .txt files found in evil corpus."

    with tempfile.TemporaryDirectory() as test_clean_out, tempfile.TemporaryDirectory() as test_evil_out:
        # Run on clean corpus
        res_clean = subprocess.run(
            [executable, target_sequence, clean_dir, test_clean_out],
            capture_output=True, text=True
        )
        assert res_clean.returncode == 0, f"Classifier failed on clean corpus:\n{res_clean.stderr}"

        # Run on evil corpus
        res_evil = subprocess.run(
            [executable, target_sequence, evil_dir, test_evil_out],
            capture_output=True, text=True
        )
        assert res_evil.returncode == 0, f"Classifier failed on evil corpus:\n{res_evil.stderr}"

        out_clean_files = set(os.listdir(test_clean_out))
        out_evil_files = set(os.listdir(test_evil_out))

        # Check clean corpus
        missing_clean = clean_files - out_clean_files
        assert not missing_clean, f"{len(missing_clean)} of {len(clean_files)} clean files modified/rejected. Offending files: {', '.join(missing_clean)}"

        # Check evil corpus
        bypassed_evil = evil_files.intersection(out_evil_files)
        assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed. Offending files: {', '.join(bypassed_evil)}"