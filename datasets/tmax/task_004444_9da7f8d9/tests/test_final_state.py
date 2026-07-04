# test_final_state.py

import os
import re
import shutil
import subprocess
import pytest

SCRIPT_PATH = "/home/user/log_sanitizer.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_OUT_DIR = "/tmp/clean_out"
EVIL_OUT_DIR = "/tmp/evil_out"

CODENAME_PATTERN = re.compile(r'(?i)operation crimson hawk')
TLS_CN_PATTERN = re.compile(re.escape(r'badguy.exfil.net'))
TOKEN_PATTERN = re.compile(r'X-Auth-Token: [A-Za-z0-9]{32}')

def apply_sanitization(text: str) -> str:
    text = CODENAME_PATTERN.sub('[REDACTED_CODENAME]', text)
    text = TLS_CN_PATTERN.sub('[REDACTED_TLS_CN]', text)
    text = TOKEN_PATTERN.sub('[REDACTED_TOKEN]', text)
    return text

@pytest.fixture(scope="session", autouse=True)
def run_sanitizer():
    assert os.path.isfile(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"

    # Setup output directories
    for d in [CLEAN_OUT_DIR, EVIL_OUT_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # Run against clean corpus
    clean_proc = subprocess.run(
        ["python3", SCRIPT_PATH, CLEAN_CORPUS_DIR, CLEAN_OUT_DIR],
        capture_output=True, text=True
    )
    assert clean_proc.returncode == 0, f"Script failed on clean corpus:\n{clean_proc.stderr}"

    # Run against evil corpus
    evil_proc = subprocess.run(
        ["python3", SCRIPT_PATH, EVIL_CORPUS_DIR, EVIL_OUT_DIR],
        capture_output=True, text=True
    )
    assert evil_proc.returncode == 0, f"Script failed on evil corpus:\n{evil_proc.stderr}"

def test_clean_corpus_preserved():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus {CLEAN_CORPUS_DIR}"

    modified_files = []
    missing_files = []

    for filename in clean_files:
        orig_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        out_path = os.path.join(CLEAN_OUT_DIR, filename)

        if not os.path.exists(out_path):
            missing_files.append(filename)
            continue

        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_content = f.read()
        with open(out_path, 'r', encoding='utf-8') as f:
            out_content = f.read()

        if orig_content != out_content:
            modified_files.append(filename)

    errors = []
    if missing_files:
        errors.append(f"{len(missing_files)} clean files missing in output: {', '.join(missing_files)}")
    if modified_files:
        errors.append(f"{len(modified_files)} of {len(clean_files)} clean files modified: {', '.join(modified_files)}")

    assert not errors, "Clean corpus validation failed:\n" + "\n".join(errors)

def test_evil_corpus_sanitized():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus {EVIL_CORPUS_DIR}"

    bypassed_files = []
    missing_files = []

    for filename in evil_files:
        orig_path = os.path.join(EVIL_CORPUS_DIR, filename)
        out_path = os.path.join(EVIL_OUT_DIR, filename)

        if not os.path.exists(out_path):
            missing_files.append(filename)
            continue

        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_content = f.read()

        expected_content = apply_sanitization(orig_content)

        with open(out_path, 'r', encoding='utf-8') as f:
            out_content = f.read()

        if expected_content != out_content:
            bypassed_files.append(filename)

    errors = []
    if missing_files:
        errors.append(f"{len(missing_files)} evil files missing in output: {', '.join(missing_files)}")
    if bypassed_files:
        errors.append(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (incorrectly sanitized): {', '.join(bypassed_files)}")

    assert not errors, "Evil corpus validation failed:\n" + "\n".join(errors)