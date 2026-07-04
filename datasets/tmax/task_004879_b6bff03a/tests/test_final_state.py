# test_final_state.py

import os
import json
import subprocess
import tarfile
import pytest

AUTH_PREFIX_PATH = "/home/user/auth_prefix.txt"
EXPECTED_PREFIX = "delta_seven_uniform_nine"
LOG_FILTER_DIR = "/home/user/log_filter"
CLEAN_CORPUS_DIR = "/app/corpora/clean/"
EVIL_CORPUS_DIR = "/app/corpora/evil/"
RAW_BACKUPS_DIR = "/app/raw_backups/"
DIFF_BACKUP_TAR = "/home/user/secure_archive/diff_backup.tar"
BACKUP_SNAR = "/home/user/secure_archive/backup.snar"

def test_auth_prefix_extracted():
    assert os.path.isfile(AUTH_PREFIX_PATH), f"Missing auth prefix file at {AUTH_PREFIX_PATH}"
    with open(AUTH_PREFIX_PATH, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_PREFIX, f"Expected auth prefix '{EXPECTED_PREFIX}', got '{content}'"

def test_rust_log_filter_compiles_and_runs():
    assert os.path.isdir(LOG_FILTER_DIR), f"Missing Rust project directory at {LOG_FILTER_DIR}"
    cargo_toml = os.path.join(LOG_FILTER_DIR, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Missing Cargo.toml in {LOG_FILTER_DIR}"

    # Check if we can build it
    res = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=LOG_FILTER_DIR,
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"Cargo build failed:\n{res.stderr}"

def test_adversarial_corpus_log_filter():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".json")]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".json")]

    clean_modified = []
    evil_bypassed = []

    for c_file in clean_files:
        path = os.path.join(CLEAN_CORPUS_DIR, c_file)
        with open(path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        res = subprocess.run(
            ["cargo", "run", "--release", "--", path],
            cwd=LOG_FILTER_DIR,
            capture_output=True,
            text=True
        )
        out_lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]

        if len(out_lines) != len(lines):
            clean_modified.append(c_file)

    for e_file in evil_files:
        path = os.path.join(EVIL_CORPUS_DIR, e_file)
        res = subprocess.run(
            ["cargo", "run", "--release", "--", path],
            cwd=LOG_FILTER_DIR,
            capture_output=True,
            text=True
        )
        out_lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]

        # Evil files should have 0 valid entries, so output should be empty
        if len(out_lines) > 0:
            evil_bypassed.append(e_file)

    err_msg = []
    if evil_bypassed:
        err_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        err_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:5])}")

    assert not err_msg, " | ".join(err_msg)

def test_bulk_file_renaming():
    files = os.listdir(RAW_BACKUPS_DIR)
    assert len(files) > 0, f"No files found in {RAW_BACKUPS_DIR}"

    for f in files:
        assert f.startswith(f"{EXPECTED_PREFIX}-"), f"File {f} in {RAW_BACKUPS_DIR} is not properly prefixed with {EXPECTED_PREFIX}-"

def test_differential_backup_archive():
    assert os.path.isfile(DIFF_BACKUP_TAR), f"Missing differential backup tar at {DIFF_BACKUP_TAR}"
    assert os.path.isfile(BACKUP_SNAR), f"Missing snapshot file at {BACKUP_SNAR}"

    with tarfile.open(DIFF_BACKUP_TAR, "r") as tar:
        names = tar.getnames()

    # Check that the files in the tar archive have the prefix
    bin_files = [n for n in names if n.endswith(".bin")]
    assert len(bin_files) > 0, "No .bin files found in the differential backup tar"

    for f in bin_files:
        basename = os.path.basename(f)
        assert basename.startswith(f"{EXPECTED_PREFIX}-"), f"Archived file {basename} is not properly prefixed"