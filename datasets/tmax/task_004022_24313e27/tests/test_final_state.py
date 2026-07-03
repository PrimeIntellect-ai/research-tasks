# test_final_state.py

import os
import subprocess
import time
import struct
import pytest

FAST_FILTER_PATH = "/home/user/fast_filter.sh"
CLEAN_CORPUS_DIR = "/home/user/corpus/clean/"
EVIL_CORPUS_DIR = "/home/user/corpus/evil/"
INCOMING_DIR = "/home/user/incoming/"
LOG_FILE = "/home/user/clean_backups.log"

def is_valid_bkp(filepath):
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(4)
            if magic != b'BKP\x00':
                return False
            length_bytes = f.read(4)
            if len(length_bytes) != 4:
                return False
            L = struct.unpack('>I', length_bytes)[0]
            metadata = f.read(L)
            if len(metadata) != L:
                return False
            if b'MALWARE' in metadata:
                return False
            for byte in metadata:
                if byte < 0x20 or byte > 0x7E:
                    return False
            return True
    except Exception:
        return False

def test_fast_filter_exists_and_executable():
    assert os.path.exists(FAST_FILTER_PATH), f"Filter script not found at {FAST_FILTER_PATH}"
    assert os.path.isfile(FAST_FILTER_PATH), f"{FAST_FILTER_PATH} is not a file"
    assert os.access(FAST_FILTER_PATH, os.X_OK), f"{FAST_FILTER_PATH} is not executable"

def test_fast_filter_adversarial_corpus():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]

    clean_failed = []
    evil_bypassed = []

    for cf in clean_files:
        res = subprocess.run([FAST_FILTER_PATH, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run([FAST_FILTER_PATH, ef], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, "Adversarial corpus checks failed:\n" + "\n".join(errors)

def test_clean_backups_log():
    assert os.path.exists(LOG_FILE), f"Log file not found at {LOG_FILE}"

    expected_files = []
    now = time.time()
    seven_days_seconds = 7 * 24 * 3600

    for root, _, files in os.walk(INCOMING_DIR):
        for f in files:
            filepath = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(filepath)
                if (now - mtime) <= seven_days_seconds:
                    if is_valid_bkp(filepath):
                        expected_files.append(filepath)
            except Exception:
                pass

    expected_files.sort()

    with open(LOG_FILE, 'r') as f:
        actual_files = [line.strip() for line in f if line.strip()]

    assert actual_files == expected_files, "The contents of clean_backups.log do not match the expected valid files modified within the last 7 days."