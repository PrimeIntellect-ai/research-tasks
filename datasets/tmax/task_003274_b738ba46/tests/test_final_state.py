# test_final_state.py

import os
import re
import numpy as np
from scipy.io import wavfile
import pytest

def test_audio_mse():
    processed = "/home/user/processed_audio.wav"
    ref = "/app/.hidden/ref_audio.wav"

    assert os.path.isfile(processed), f"Missing processed audio file: {processed}"
    assert os.path.isfile(ref), f"Missing reference audio file: {ref}"

    try:
        sr1, audio1 = wavfile.read(processed)
        sr2, audio2 = wavfile.read(ref)
    except Exception as e:
        pytest.fail(f"Could not read audio files: {e}")

    assert sr1 == 16000, f"Sample rate mismatch: expected 16000, got {sr1}"
    assert sr1 == sr2, f"Sample rate mismatch with reference: expected {sr2}, got {sr1}"

    # Normalize integer audio to float for MSE calculation
    if np.issubdtype(audio1.dtype, np.integer):
        audio1 = audio1.astype(np.float32) / np.iinfo(audio1.dtype).max
    else:
        audio1 = audio1.astype(np.float32)

    if np.issubdtype(audio2.dtype, np.integer):
        audio2 = audio2.astype(np.float32) / np.iinfo(audio2.dtype).max
    else:
        audio2 = audio2.astype(np.float32)

    # Ensure mono
    if len(audio1.shape) > 1:
        audio1 = audio1.mean(axis=1)
    if len(audio2.shape) > 1:
        audio2 = audio2.mean(axis=1)

    min_len = min(len(audio1), len(audio2))
    audio1 = audio1[:min_len]
    audio2 = audio2[:min_len]

    mse = np.mean((audio1 - audio2) ** 2)
    assert mse <= 0.005, f"FAIL: MSE {mse} exceeds threshold 0.005"

def test_csv_cleaning():
    clean_path = "/home/user/metadata_clean.csv"
    assert os.path.isfile(clean_path), f"Missing clean CSV file: {clean_path}"

    with open(clean_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    assert len(lines) > 1, "CSV file is empty or missing data rows"

    header = lines[0]
    data_lines = lines[1:]

    seen_texts = set()

    for i, line in enumerate(data_lines):
        # 1. Check that every row starts with an integer ID and a timestamp
        match = re.match(r'^(\d+),(\d{2}:\d{2}:\d{2}(?:\.\d+)?),(.+)$', line)
        assert match is not None, f"Row {i+1} is malformed or contains embedded newlines: {line}"

        row_id, timestamp, text = match.groups()

        # 2. Check that the text column is fully lowercase
        assert text == text.lower(), f"Row {i+1} text is not fully lowercase: {text}"

        # 3. Check for duplicates in the text column
        assert text not in seen_texts, f"Duplicate text found in row {i+1}: {text}"
        seen_texts.add(text)