# test_final_state.py
import os
import subprocess
import pytest

def test_voicemail_transcription():
    transcript_path = "/home/user/voicemail_transcript.txt"
    assert os.path.exists(transcript_path), f"Transcript file missing: {transcript_path}"

    with open(transcript_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    keywords = ["linker", "undefined", "reference", "sqlite3"]
    missing = [kw for kw in keywords if kw not in content]
    assert not missing, f"Transcript is missing expected keywords: {missing}. Content found: {content}"

def test_classifier_clean_corpus():
    script_path = "/home/user/classifier.py"
    clean_dir = "/app/corpus/clean/"
    assert os.path.exists(script_path), f"Classifier script missing: {script_path}"

    result = subprocess.run(["python3", script_path, clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Classifier script failed on clean corpus: {result.stderr}"

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    expected_files = {f for f in os.listdir(clean_dir) if f.endswith(".txt")}

    processed_files = set()
    bypassed = []

    for line in lines:
        if ":" not in line:
            continue
        filename, classification = line.split(":", 1)
        filename = filename.strip()
        classification = classification.strip()

        if filename in expected_files:
            processed_files.add(filename)
            if classification != "CLEAN":
                bypassed.append(filename)

    missing = expected_files - processed_files
    assert not missing, f"Classifier missed clean files: {missing}"
    assert not bypassed, f"{len(bypassed)} of {len(expected_files)} clean modified (classified as EVIL): {bypassed}"

def test_classifier_evil_corpus():
    script_path = "/home/user/classifier.py"
    evil_dir = "/app/corpus/evil/"
    assert os.path.exists(script_path), f"Classifier script missing: {script_path}"

    result = subprocess.run(["python3", script_path, evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Classifier script failed on evil corpus: {result.stderr}"

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    expected_files = {f for f in os.listdir(evil_dir) if f.endswith(".txt")}

    processed_files = set()
    bypassed = []

    for line in lines:
        if ":" not in line:
            continue
        filename, classification = line.split(":", 1)
        filename = filename.strip()
        classification = classification.strip()

        if filename in expected_files:
            processed_files.add(filename)
            if classification != "EVIL":
                bypassed.append(filename)

    missing = expected_files - processed_files
    assert not missing, f"Classifier missed evil files: {missing}"
    assert not bypassed, f"{len(bypassed)} of {len(expected_files)} evil bypassed (classified as CLEAN): {bypassed}"