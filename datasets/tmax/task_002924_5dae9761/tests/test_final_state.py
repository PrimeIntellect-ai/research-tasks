# test_final_state.py

import os
import subprocess
import urllib.parse
import pytest

SCRIPT_PATH = "/home/user/build_orchestrator.py"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def parse_url(url_str):
    # build://{action}?token={BUILD_TOKEN}&target={target_name}&flags={compiler_flags}
    if not url_str.startswith("build://"):
        return None, None, None
    url_str = url_str[8:]
    if "?" not in url_str:
        return None, None, None
    action, query = url_str.split("?", 1)
    params = urllib.parse.parse_qs(query, keep_blank_values=True)
    target = params.get("target", [""])[0]
    flags = params.get("flags", [""])[0]
    return action, target, flags

def test_build_orchestrator_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"

def test_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus missing at {CLEAN_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith(".txt")]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        with open(filepath, "r") as f:
            url_str = f.read().strip()

        action, target, flags = parse_url(url_str)
        expected_output = f"ACCEPT: [{action}] built {target} with {flags}"

        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--verify", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            stdout = result.stdout.strip()
            if stdout != expected_output:
                failed_files.append((filename, stdout, expected_output))
        except Exception as e:
            failed_files.append((filename, str(e), expected_output))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(clean_files)} clean modified/rejected.\n"
        for f, out, exp in failed_files:
            error_msg += f"File: {f} | Expected: '{exp}' | Got: '{out}'\n"
        pytest.fail(error_msg)

def test_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus missing at {EVIL_DIR}"
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith(".txt")]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)

        try:
            result = subprocess.run(
                ["python3", SCRIPT_PATH, "--verify", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            stdout = result.stdout.strip()
            if stdout != "REJECT":
                failed_files.append((filename, stdout))
        except Exception as e:
            failed_files.append((filename, str(e)))

    if failed_files:
        error_msg = f"{len(failed_files)} of {len(evil_files)} evil bypassed.\n"
        for f, out in failed_files:
            error_msg += f"File: {f} | Got: '{out}' instead of 'REJECT'\n"
        pytest.fail(error_msg)