# test_final_state.py

import os
import stat
import subprocess
import pytest

VALIDATE_SCRIPT = "/home/user/validate_payload"
SUPERVISOR_SCRIPT = "/home/user/supervisor.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
SPOOL_INCOMING = "/home/user/spool/incoming"
SPOOL_PROCESSED = "/home/user/spool/processed"
SPOOL_QUARANTINE = "/home/user/spool/quarantine"

def test_validate_payload_exists_and_executable():
    assert os.path.exists(VALIDATE_SCRIPT), f"{VALIDATE_SCRIPT} does not exist."
    assert os.path.isfile(VALIDATE_SCRIPT), f"{VALIDATE_SCRIPT} is not a file."
    assert os.access(VALIDATE_SCRIPT, os.X_OK), f"{VALIDATE_SCRIPT} is not executable."

def test_supervisor_script_exists_and_executable():
    assert os.path.exists(SUPERVISOR_SCRIPT), f"{SUPERVISOR_SCRIPT} does not exist."
    assert os.path.isfile(SUPERVISOR_SCRIPT), f"{SUPERVISOR_SCRIPT} is not a file."
    assert os.access(SUPERVISOR_SCRIPT, os.X_OK), f"{SUPERVISOR_SCRIPT} is not executable."

def test_spool_directories_and_permissions():
    for d in [SPOOL_INCOMING, SPOOL_PROCESSED, SPOOL_QUARANTINE]:
        assert os.path.exists(d), f"Directory {d} does not exist."
        assert os.path.isdir(d), f"{d} is not a directory."

    incoming_stat = os.stat(SPOOL_INCOMING)
    perms = stat.S_IMODE(incoming_stat.st_mode)
    assert perms == 0o733, f"Permissions of {SPOOL_INCOMING} are {oct(perms)}, expected 0o733."

def test_adversarial_corpus_clean():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert clean_files, f"No files found in clean corpus {CLEAN_CORPUS_DIR}"

    failed_files = []
    for f in clean_files:
        result = subprocess.run([VALIDATE_SCRIPT, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (should be accepted). Offending files: {', '.join(failed_files)}")

def test_adversarial_corpus_evil():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert evil_files, f"No files found in evil corpus {EVIL_CORPUS_DIR}"

    failed_files = []
    for f in evil_files:
        result = subprocess.run([VALIDATE_SCRIPT, f], capture_output=True)
        if result.returncode == 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (should be rejected). Offending files: {', '.join(failed_files)}")