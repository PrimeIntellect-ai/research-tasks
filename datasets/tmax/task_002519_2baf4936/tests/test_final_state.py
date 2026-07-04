# test_final_state.py

import os
import subprocess
import pytest

CLASSIFIER_PATH = "/home/user/classifier"
EVIL_CORPUS = "/app/verifier_corpus/evil"
CLEAN_CORPUS = "/app/verifier_corpus/clean"
INCOMING_CORPUS = "/app/corpus/incoming"
VERIFIED_DIR = "/home/user/repo_verified"
QUARANTINE_DIR = "/home/user/repo_quarantine"
SIGNATURE = b"\xDE\xAD\xBE\xEF\x42\x13\x37"

def test_classifier_exists():
    assert os.path.isfile(CLASSIFIER_PATH), f"Classifier binary not found at {CLASSIFIER_PATH}"
    assert os.access(CLASSIFIER_PATH, os.X_OK), f"Classifier at {CLASSIFIER_PATH} is not executable"

def test_adversarial_corpus_clean():
    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    failed_clean = []

    for fpath in clean_files:
        result = subprocess.run([CLASSIFIER_PATH, fpath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(fpath))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean files rejected (exit code != 0): {failed_clean[:5]}..."

def test_adversarial_corpus_evil():
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    failed_evil = []

    for fpath in evil_files:
        result = subprocess.run([CLASSIFIER_PATH, fpath], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(fpath))

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (exit code != 1): {failed_evil[:5]}..."

def test_incoming_corpus_processing():
    assert os.path.isdir(VERIFIED_DIR), f"{VERIFIED_DIR} directory is missing"
    assert os.path.isdir(QUARANTINE_DIR), f"{QUARANTINE_DIR} directory is missing"

    clean_expected = []
    evil_expected = []

    for root, _, files in os.walk(INCOMING_CORPUS):
        for file in files:
            fpath = os.path.join(root, file)
            with open(fpath, "rb") as f:
                content = f.read()
            if SIGNATURE in content:
                evil_expected.append(fpath)
            else:
                clean_expected.append(fpath)

    verified_files = os.listdir(VERIFIED_DIR)
    quarantine_files = os.listdir(QUARANTINE_DIR)

    assert len(verified_files) == len(clean_expected), f"Expected {len(clean_expected)} files in verified repo, found {len(verified_files)}"
    assert len(quarantine_files) == len(evil_expected), f"Expected {len(evil_expected)} files in quarantine repo, found {len(quarantine_files)}"

    for clean_fpath in clean_expected:
        basename = os.path.basename(clean_fpath)
        verified_fpath = os.path.join(VERIFIED_DIR, basename)
        assert os.path.exists(verified_fpath), f"Missing verified file: {basename}"
        assert os.stat(clean_fpath).st_ino == os.stat(verified_fpath).st_ino, f"{verified_fpath} is not a hard link to {clean_fpath}"

    for evil_fpath in evil_expected:
        basename = os.path.basename(evil_fpath)
        quarantine_fpath = os.path.join(QUARANTINE_DIR, basename)
        assert os.path.islink(quarantine_fpath), f"{quarantine_fpath} is not a symbolic link"
        assert os.readlink(quarantine_fpath) == evil_fpath, f"{quarantine_fpath} does not point to {evil_fpath}"