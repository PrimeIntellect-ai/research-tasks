# test_final_state.py
import os
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/detector.sh"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"

def test_detector_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Missing agent script at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"{AGENT_SCRIPT} is not executable"

def run_detector(filepath):
    try:
        result = subprocess.run(
            [AGENT_SCRIPT, filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS_DIR) and os.path.isdir(EVIL_CORPUS_DIR), f"Missing evil corpus at {EVIL_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.jsonl')]
    assert len(evil_files) > 0, "No JSONL files found in evil corpus"

    bypassed = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        output = run_detector(filepath)
        if output != "EVIL":
            bypassed.append((filename, output))

    if bypassed:
        details = ", ".join([f"{f} (output: {out})" for f, out in bypassed[:5]])
        if len(bypassed) > 5:
            details += f" ... and {len(bypassed) - 5} more"
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil files bypassed detection. Examples: {details}")

def test_clean_corpus_accepted():
    assert os.path.exists(CLEAN_CORPUS_DIR) and os.path.isdir(CLEAN_CORPUS_DIR), f"Missing clean corpus at {CLEAN_CORPUS_DIR}"

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.jsonl')]
    assert len(clean_files) > 0, "No JSONL files found in clean corpus"

    modified = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        output = run_detector(filepath)
        if output != "CLEAN":
            modified.append((filename, output))

    if modified:
        details = ", ".join([f"{f} (output: {out})" for f, out in modified[:5]])
        if len(modified) > 5:
            details += f" ... and {len(modified) - 5} more"
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean files were incorrectly flagged/modified. Examples: {details}")