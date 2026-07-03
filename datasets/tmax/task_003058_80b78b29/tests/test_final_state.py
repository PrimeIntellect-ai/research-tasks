# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sequence_classifier.sh"
CLEAN_CORPUS = "/app/data/clean"
EVIL_CORPUS = "/app/data/evil"
REJECTED_LOG = "/home/user/rejected.log"

TEST_CLEAN_OUT = "/home/user/test_clean_out"
TEST_EVIL_OUT = "/home/user/test_evil_out"

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    """Runs the student's script against both corpora before tests."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    os.makedirs(TEST_CLEAN_OUT, exist_ok=True)
    os.makedirs(TEST_EVIL_OUT, exist_ok=True)

    # Remove rejected log if it exists from previous runs
    if os.path.exists(REJECTED_LOG):
        os.remove(REJECTED_LOG)

    # Run against clean corpus
    result_clean = subprocess.run(
        ["bash", SCRIPT_PATH, CLEAN_CORPUS, TEST_CLEAN_OUT],
        capture_output=True, text=True
    )
    assert result_clean.returncode == 0, f"Script failed on clean corpus:\n{result_clean.stderr}"

    # Run against evil corpus
    result_evil = subprocess.run(
        ["bash", SCRIPT_PATH, EVIL_CORPUS, TEST_EVIL_OUT],
        capture_output=True, text=True
    )
    assert result_evil.returncode == 0, f"Script failed on evil corpus:\n{result_evil.stderr}"

def test_clean_corpus_preserved():
    """Test that all clean files are preserved in the output directory."""
    clean_files = [os.path.basename(f) for f in glob.glob(os.path.join(CLEAN_CORPUS, "*.fasta"))]
    out_files = [os.path.basename(f) for f in glob.glob(os.path.join(TEST_CLEAN_OUT, "*.fasta"))]

    missing = set(clean_files) - set(out_files)
    modified = set(out_files) - set(clean_files)

    assert not missing, f"{len(missing)} of {len(clean_files)} clean files were not preserved. Missing: {missing}"
    assert not modified, f"Unexpected files found in clean output: {modified}"

def test_evil_corpus_rejected():
    """Test that all evil files are rejected and not copied to the output directory."""
    evil_files = [os.path.basename(f) for f in glob.glob(os.path.join(EVIL_CORPUS, "*.fasta"))]
    out_files = [os.path.basename(f) for f in glob.glob(os.path.join(TEST_EVIL_OUT, "*.fasta"))]

    bypassed = set(out_files).intersection(set(evil_files))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil files bypassed the filter. Bypassed: {bypassed}"
    assert len(out_files) == 0, f"Evil output directory should be empty, found: {out_files}"

def test_rejected_log():
    """Test that the rejected.log contains the basenames of all evil files."""
    assert os.path.isfile(REJECTED_LOG), f"Rejected log not found at {REJECTED_LOG}"

    with open(REJECTED_LOG, "r") as f:
        log_contents = f.read()

    evil_files = [os.path.basename(f) for f in glob.glob(os.path.join(EVIL_CORPUS, "*.fasta"))]

    missing_from_log = []
    for evil_file in evil_files:
        if evil_file not in log_contents:
            missing_from_log.append(evil_file)

    assert not missing_from_log, f"The following evil files were not found in {REJECTED_LOG}: {missing_from_log}"