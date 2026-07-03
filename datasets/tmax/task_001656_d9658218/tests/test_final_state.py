# test_final_state.py

import os
import json
import wave
import struct
import tempfile
import requests
import pytest

def test_evidence_result():
    evidence_path = "/app/evidence.wav"
    result_path = "/home/user/evidence_result.json"

    assert os.path.exists(result_path), f"File {result_path} does not exist. Did you save the result of evidence.wav?"

    with wave.open(evidence_path, 'rb') as w:
        frames = w.getnframes()
        rate = w.getframerate()
        expected_duration = frames / rate
        expected_samples = frames

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("samples") == expected_samples, f"Expected {expected_samples} samples, got {data.get('samples')}"
    assert abs(data.get("duration", 0) - expected_duration) < 1e-4, f"Expected duration ~{expected_duration}, got {data.get('duration')}"

def create_test_wav_with_fact_chunk(filepath):
    num_channels = 1
    sample_width = 2
    framerate = 44100
    num_frames = 44100  # exactly 1 second

    audio_data = b'\x00\x00' * num_frames

    fmt_chunk = struct.pack('<HHIIHH', 1, num_channels, framerate, framerate * num_channels * sample_width, num_channels * sample_width, sample_width * 8)
    fmt_chunk_full = b'fmt ' + struct.pack('<I', len(fmt_chunk)) + fmt_chunk

    fact_chunk_data = struct.pack('<I', num_frames)
    fact_chunk_full = b'fact' + struct.pack('<I', len(fact_chunk_data)) + fact_chunk_data

    data_chunk_full = b'data' + struct.pack('<I', len(audio_data)) + audio_data

    riff_data = b'WAVE' + fmt_chunk_full + fact_chunk_full + data_chunk_full
    riff_chunk_full = b'RIFF' + struct.pack('<I', len(riff_data)) + riff_data

    with open(filepath, 'wb') as f:
        f.write(riff_chunk_full)

    return 1.0, num_frames

def test_service_analyze_with_fact_chunk():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        filepath = tmp.name

    try:
        expected_duration, expected_samples = create_test_wav_with_fact_chunk(filepath)

        with open(filepath, 'rb') as f:
            files = {'audio': ('test_fact.wav', f, 'audio/wav')}
            try:
                response = requests.post('http://127.0.0.1:8000/analyze', files=files, timeout=5)
            except requests.exceptions.RequestException as e:
                pytest.fail(f"Failed to connect to the service at 127.0.0.1:8000: {e}")

        assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Service did not return valid JSON. Response text: {response.text}")

        assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
        assert data.get("samples") == expected_samples, f"Expected {expected_samples} samples, got {data.get('samples')}"
        assert abs(data.get("duration", 0) - expected_duration) < 1e-4, f"Expected duration ~{expected_duration}, got {data.get('duration')}"
    finally:
        os.remove(filepath)