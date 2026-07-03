# test_final_state.py

import os
import re
import subprocess
from pathlib import Path
import pytest

DETECTOR_SCRIPT = "/home/user/detector.sh"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"
LOG_FILE = "/home/user/pipeline.log"

def test_detector_exists_and_executable():
    assert os.path.exists(DETECTOR_SCRIPT), f"Detector script {DETECTOR_SCRIPT} does not exist."
    assert os.path.isfile(DETECTOR_SCRIPT), f"{DETECTOR_SCRIPT} is not a file."
    assert os.access(DETECTOR_SCRIPT, os.X_OK), f"Detector script {DETECTOR_SCRIPT} is not executable."

def test_corpus_classification():
    clean_files = list(Path(CLEAN_CORPUS).glob("*"))
    evil_files = list(Path(EVIL_CORPUS).glob("*"))

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([DETECTOR_SCRIPT, str(cf)], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(cf.name)

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([DETECTOR_SCRIPT, str(ef)], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(ef.name)

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean files modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil files bypassed: {', '.join(evil_failed)}")

    assert not error_msg, " | ".join(error_msg)

def test_pipeline_log_format():
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} is not a file."

    with open(LOG_FILE, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"Log file {LOG_FILE} is empty."

    log_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] FILE=[\w.-]+ STATUS=(CLEAN|EVIL)$")

    invalid_lines = []
    for line in lines:
        if not log_pattern.match(line):
            invalid_lines.append(line)

    assert not invalid_lines, f"Found {len(invalid_lines)} invalid log lines. Example: {invalid_lines[0]}"