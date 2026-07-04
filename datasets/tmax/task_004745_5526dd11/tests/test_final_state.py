# test_final_state.py

import os
import subprocess
import string
import pytest

def normalize_text(text):
    """Normalize text by removing punctuation and converting to lowercase."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return ' '.join(text.split())

def test_etl_script_exists_and_executable():
    script_path = "/home/user/process_audio.sh"
    assert os.path.isfile(script_path), f"ETL script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"ETL script {script_path} is not executable."

def test_etl_output_correct():
    script_path = "/home/user/process_audio.sh"
    audio_path = "/app/audio/support_call.wav"
    log_path = "/home/user/etl_output.log"

    # Run the script to ensure it processes the audio
    # If the student already ran it, this will append another line, which is fine as we check the last line.
    try:
        subprocess.run([script_path, audio_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"process_audio.sh failed with exit code {e.returncode}. Stderr: {e.stderr}")

    assert os.path.isfile(log_path), f"ETL output log {log_path} was not created."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) > 0, f"ETL output log {log_path} is empty."

    last_line = lines[-1]
    parts = [p.strip() for p in last_line.split('|')]

    assert len(parts) >= 3, f"ETL output log line format incorrect. Expected '[customer_id] | [account_tier] | [TRANSCRIPT_TEXT]', got: {last_line}"

    customer_id = parts[0]
    account_tier = parts[1]
    transcript = " ".join(parts[2:])

    assert customer_id == "CUST-9921", f"Expected customer_id 'CUST-9921', got '{customer_id}'"
    assert account_tier == "Premium", f"Expected account_tier 'Premium', got '{account_tier}'"

    expected_transcript = "hello i am locked out of my account and need a password reset thank you"
    normalized_transcript = normalize_text(transcript)

    assert expected_transcript in normalized_transcript or normalized_transcript in expected_transcript, \
        f"Transcript text does not match expected output. Got: '{transcript}'"

def test_filter_script_exists_and_executable():
    filter_path = "/home/user/filter.sh"
    assert os.path.isfile(filter_path), f"Filter script {filter_path} does not exist."
    assert os.access(filter_path, os.X_OK), f"Filter script {filter_path} is not executable."

def test_adversarial_corpus_filter():
    filter_path = "/home/user/filter.sh"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} does not exist."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} does not exist."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_bypassed = []
    for cf in clean_files:
        result = subprocess.run([filter_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_bypassed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run([filter_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_bypassed:
        errors.append(f"{len(clean_bypassed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))