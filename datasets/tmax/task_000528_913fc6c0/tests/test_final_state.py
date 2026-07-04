# test_final_state.py
import os
import subprocess
import sys

def test_detector_script():
    script_path = "/home/user/detector.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

    evil_corpus_path = "/app/corpus/evil.txt"
    clean_corpus_path = "/app/corpus/clean.txt"

    assert os.path.isfile(evil_corpus_path), f"Missing evil corpus at {evil_corpus_path}"
    assert os.path.isfile(clean_corpus_path), f"Missing clean corpus at {clean_corpus_path}"

    with open(evil_corpus_path, "r", encoding="utf-8") as f:
        evil_payloads = f.read().splitlines()

    with open(clean_corpus_path, "r", encoding="utf-8") as f:
        clean_payloads = f.read().splitlines()

    evil_failures = []
    for payload in evil_payloads:
        result = subprocess.run(
            [sys.executable, script_path, payload],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "REJECTED_OVERLORD":
            evil_failures.append((payload, result.returncode, stdout))

    clean_failures = []
    for payload in clean_payloads:
        result = subprocess.run(
            [sys.executable, script_path, payload],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "SAFE":
            clean_failures.append((payload, result.returncode, stdout))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_payloads)} evil payloads bypassed.")
        for payload, rc, out in evil_failures[:5]:
            errors.append(f"  Evil payload bypassed: {repr(payload)} -> exit {rc}, stdout {repr(out)}")

    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_payloads)} clean payloads rejected/modified.")
        for payload, rc, out in clean_failures[:5]:
            errors.append(f"  Clean payload rejected: {repr(payload)} -> exit {rc}, stdout {repr(out)}")

    assert not errors, "\n".join(errors)