# test_final_state.py

import os
import subprocess
import tarfile
import pytest

SCRIPT_PATH = "/home/user/config_sanitizer.py"
ARCHIVE_PATH = "/home/user/clean_configs.tar.gz"
EVIL_CORPUS_DIR = "/app/tests/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/tests/corpus/clean/"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_adversarial_corpus_evil():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'rb') as f:
            result = subprocess.run(["python3", SCRIPT_PATH], stdin=f, capture_output=True)
            if result.returncode != 1:
                bypassed_files.append(filename)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"

def test_adversarial_corpus_clean():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'rb') as f:
            result = subprocess.run(["python3", SCRIPT_PATH], stdin=f, capture_output=True)
            if result.returncode != 0:
                modified_files.append(filename)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean modified/rejected: {', '.join(modified_files)}"

def test_archive_exists_and_contents():
    assert os.path.exists(ARCHIVE_PATH), f"Archive missing at {ARCHIVE_PATH}"
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive"

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getnames()
        # Strip any leading directories if the user archived them with paths
        basenames = [os.path.basename(m) for m in members if not m.endswith('/')]

        expected_files = {"nginx.conf", "app_config.json"}
        actual_files = set(basenames)

        missing = expected_files - actual_files
        extra = actual_files - expected_files

        assert not missing, f"Missing expected clean configs in archive: {', '.join(missing)}"
        assert not extra, f"Archive contains unexpected files (evil configs or others): {', '.join(extra)}"