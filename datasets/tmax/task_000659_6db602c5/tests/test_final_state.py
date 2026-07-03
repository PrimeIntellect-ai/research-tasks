# test_final_state.py

import os
import json
import re
import pytest

def test_audio_transcription():
    transcript_path = "/home/user/audio_transcript.txt"
    assert os.path.isfile(transcript_path), f"Missing transcript file: {transcript_path}"

    with open(transcript_path, 'r') as f:
        content = f.read().lower()

    # Strip punctuation for flexible matching
    content = re.sub(r'[^\w\s]', '', content)
    expected = "Subject confirmed the anomaly originates from sector 7G".lower()
    expected = re.sub(r'[^\w\s]', '', expected)

    assert expected in content, f"Transcript does not contain the expected text. Expected: {expected}"

def test_adversarial_corpus_processing():
    evil_dir = "/app/corpora/incoming/evil"
    clean_dir = "/app/corpora/incoming/clean"
    output_dir = "/home/user/extracted_datasets"
    rejected_log = "/home/user/rejected_archives.log"

    assert os.path.isfile(rejected_log), f"Missing rejected archives log: {rejected_log}"
    with open(rejected_log, 'r') as f:
        rejected_files = [line.strip() for line in f.readlines() if line.strip()]

    evil_zips = [f for f in os.listdir(evil_dir) if f.endswith('.zip')] if os.path.isdir(evil_dir) else []
    clean_zips = [f for f in os.listdir(clean_dir) if f.endswith('.zip')] if os.path.isdir(clean_dir) else []

    # Check evil zips
    evil_bypassed = []
    for evil in evil_zips:
        if evil not in rejected_files:
            evil_bypassed.append(evil)

        # Ensure it wasn't extracted
        basename = evil[:-4]
        if os.path.exists(os.path.join(output_dir, basename)):
            evil_bypassed.append(evil + " (extracted)")

    assert not evil_bypassed, f"{len(evil_bypassed)} of {len(evil_zips)} evil bypassed: {evil_bypassed}"

    # Check clean zips
    clean_modified = []
    for clean in clean_zips:
        if clean in rejected_files:
            clean_modified.append(clean + " (rejected)")
            continue

        basename = clean[:-4]
        extracted_path = os.path.join(output_dir, basename)
        if not os.path.isdir(extracted_path):
            clean_modified.append(clean + " (not extracted)")
            continue

        json_path = os.path.join(extracted_path, "events.json")
        if not os.path.isfile(json_path):
            clean_modified.append(clean + " (missing events.json)")
            continue

        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    clean_modified.append(clean + " (events.json is not a list)")
        except json.JSONDecodeError:
            clean_modified.append(clean + " (invalid JSON)")

    assert not clean_modified, f"{len(clean_modified)} of {len(clean_zips)} clean modified/failed: {clean_modified}"