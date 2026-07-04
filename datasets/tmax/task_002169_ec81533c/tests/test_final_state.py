# test_final_state.py
import os
import glob
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/filter.sh"
CLEAN_CORPUS_DIR = "/test_corpus/clean"
EVIL_CORPUS_DIR = "/test_corpus/evil"

def test_filter_script_exists_and_executable():
    assert os.path.exists(FILTER_SCRIPT), f"Solution script {FILTER_SCRIPT} is missing."
    assert os.access(FILTER_SCRIPT, os.X_OK), f"Solution script {FILTER_SCRIPT} is not executable."

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_modified = []
    evil_bypassed = []

    for f in clean_files:
        out_f = f"/tmp/clean_out_{os.path.basename(f)}"
        try:
            subprocess.run([FILTER_SCRIPT, f, out_f], check=True, capture_output=True, timeout=30)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script failed on clean file {f}: {e.stderr.decode()}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Script timed out on clean file {f}")

        with open(f, "r") as infile:
            in_lines = infile.readlines()

        if not os.path.exists(out_f):
            clean_modified.append(os.path.basename(f))
            continue

        with open(out_f, "r") as outfile:
            out_lines = outfile.readlines()

        if len(in_lines) != len(out_lines):
            clean_modified.append(os.path.basename(f))

    for f in evil_files:
        out_f = f"/tmp/evil_out_{os.path.basename(f)}"
        try:
            subprocess.run([FILTER_SCRIPT, f, out_f], check=True, capture_output=True, timeout=30)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script failed on evil file {f}: {e.stderr.decode()}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Script timed out on evil file {f}")

        if not os.path.exists(out_f):
            evil_bypassed.append(os.path.basename(f))
            continue

        with open(out_f, "r") as outfile:
            out_lines = outfile.readlines()

        if len(out_lines) != 1 or out_lines[0].strip() != "id,text":
            evil_bypassed.append(os.path.basename(f))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))