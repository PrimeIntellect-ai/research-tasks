# test_final_state.py

import os
import difflib
import pytest

def test_recovered_wav_exists():
    path = "/home/user/recovered.wav"
    assert os.path.isfile(path), f"Required file {path} was not created."

def test_watcher_script_exists():
    path = "/home/user/watcher.py"
    assert os.path.isfile(path), f"Required script {path} was not created."

def test_transcription_accuracy():
    agent_file = "/home/user/firewall_rules.txt"
    truth_file = "/app/artefact.txt"

    assert os.path.isfile(agent_file), f"Transcription output file {agent_file} is missing."
    assert os.path.isfile(truth_file), f"Ground truth file {truth_file} is missing."

    with open(agent_file, "r", encoding="utf-8") as f:
        agent_text = f.read().strip().lower()

    with open(truth_file, "r", encoding="utf-8") as f:
        truth_text = f.read().strip().lower()

    # Using difflib.SequenceMatcher to approximate Levenshtein ratio using standard library
    ratio = difflib.SequenceMatcher(None, agent_text, truth_text).ratio()

    assert ratio >= 0.75, f"Transcription accuracy is too low. Expected ratio >= 0.75, got {ratio:.4f}"