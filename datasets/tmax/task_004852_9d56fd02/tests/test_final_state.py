# test_final_state.py
import os
import json
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/payload_detector.py"
REPORT_FILE = "/home/user/report.json"
EVIL_DIR = "/app/corpora/evil/"
CLEAN_DIR = "/app/corpora/clean/"

def run_agent_script(corpus_dir):
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)

    result = subprocess.run(
        ["python3", AGENT_SCRIPT, corpus_dir],
        capture_output=True,
        text=True
    )
    return result

def test_payload_detector_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"Expected a file at {AGENT_SCRIPT}"

def test_evil_corpus_classification():
    assert os.path.exists(EVIL_DIR), f"Evil corpus missing at {EVIL_DIR}"

    run_agent_script(EVIL_DIR)

    assert os.path.exists(REPORT_FILE), f"Report file missing at {REPORT_FILE} after running script on evil corpus."

    with open(REPORT_FILE, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_FILE} is not valid JSON.")

    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    bypassed_files = []
    missing_files = []

    for f in evil_files:
        if f not in report:
            missing_files.append(f)
        elif report[f] != "evil":
            bypassed_files.append(f)

    error_msg = ""
    if bypassed_files:
        error_msg += f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}. "
    if missing_files:
        error_msg += f"{len(missing_files)} files missing from report: {', '.join(missing_files)}."

    if error_msg:
        pytest.fail(error_msg.strip())

def test_clean_corpus_classification():
    assert os.path.exists(CLEAN_DIR), f"Clean corpus missing at {CLEAN_DIR}"

    run_agent_script(CLEAN_DIR)

    assert os.path.exists(REPORT_FILE), f"Report file missing at {REPORT_FILE} after running script on clean corpus."

    with open(REPORT_FILE, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_FILE} is not valid JSON.")

    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]

    modified_files = []
    missing_files = []

    for f in clean_files:
        if f not in report:
            missing_files.append(f)
        elif report[f] != "clean":
            modified_files.append(f)

    error_msg = ""
    if modified_files:
        error_msg += f"{len(modified_files)} of {len(clean_files)} clean modified (classified as evil or other): {', '.join(modified_files)}. "
    if missing_files:
        error_msg += f"{len(missing_files)} files missing from report: {', '.join(missing_files)}."

    if error_msg:
        pytest.fail(error_msg.strip())