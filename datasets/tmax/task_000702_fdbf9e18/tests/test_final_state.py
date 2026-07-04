# test_final_state.py

import os
import gzip
import pytest

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def compute_cer(reference, hypothesis):
    ref_len = len(reference)
    if ref_len == 0:
        return 1.0
    distance = levenshtein_distance(reference, hypothesis)
    return distance / ref_len

def test_transcription_accuracy():
    transcript_path = '/home/user/transcripts/voicemail.txt'
    assert os.path.exists(transcript_path), f"Transcript file not found at {transcript_path}"

    ground_truth = "the disk quota has been exceeded on the primary storage volume please allocate additional drives to the raid array immediately to prevent data loss"

    with open(transcript_path, 'r') as f:
        agent_text = f.read().strip().lower()

    for char in ".,!?":
        agent_text = agent_text.replace(char, "")

    cer = compute_cer(ground_truth, agent_text)
    assert cer <= 0.15, f"Transcription CER is {cer:.3f}, which exceeds the threshold of 0.15. Ground truth: '{ground_truth}', Agent output: '{agent_text}'"

def test_archived_server_1_log():
    archive_path = '/home/user/archive_dir/server_1.log.gz'
    assert os.path.exists(archive_path), f"Archived file not found at {archive_path}"

    with gzip.open(archive_path, 'rt') as f:
        content = f.read()

    assert "[DEBUG]" not in content, f"[DEBUG] lines were not filtered out in {archive_path}"
    assert "[ERROR]" in content, f"[ERROR] lines were incorrectly filtered out in {archive_path}"
    assert "[INFO]" in content, f"[INFO] lines were incorrectly filtered out in {archive_path}"

def test_archived_app_server_log():
    archive_path = '/home/user/archive_dir/app_server.log.gz'
    assert os.path.exists(archive_path), f"Archived file not found at {archive_path}"

    with gzip.open(archive_path, 'rt') as f:
        content = f.read()

    assert "[DEBUG]" not in content, f"[DEBUG] lines were not filtered out in {archive_path}"
    assert "[INFO] App started" in content, f"Expected content missing in {archive_path}"
    assert "[INFO] Connected to DB" in content, f"Expected content missing in {archive_path}"

def test_bash_script_exists():
    script_path = '/home/user/archive.sh'
    assert os.path.exists(script_path), f"Bash script not found at {script_path}"