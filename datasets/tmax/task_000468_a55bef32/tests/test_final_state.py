# test_final_state.py

import os
import re
import wave
import hashlib
import json
import pytest
import requests

def test_api_and_audio_processing():
    """
    Validates that the HTTP API is running and returns the correct transcription,
    and that the processed audio files match the requirements.
    """
    # 1. Check HTTP API
    url = "http://127.0.0.1:8000/api/dataset"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP API at {url}. Is the service running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert isinstance(data, dict), f"Expected JSON response to be a dictionary, got {type(data)}"
    assert len(data) > 0, "The dataset API returned an empty dictionary, expected at least one entry."

    # 2. Validate JSON keys and transcription content
    filename_regex = re.compile(r"^field_record_[a-f0-9]{32}\.wav$")
    found_target_transcript = False

    for filename, transcript in data.items():
        assert filename_regex.match(filename), f"Filename '{filename}' does not match the required format 'field_record_<md5>.wav'"
        assert isinstance(transcript, str), f"Expected transcript for '{filename}' to be a string, got {type(transcript)}"

        transcript_lower = transcript.lower()
        if "blue-winged warbler" in transcript_lower and "northern creek" in transcript_lower:
            found_target_transcript = True

    assert found_target_transcript, "None of the transcripts contained the expected phrases ('blue-winged warbler' and 'northern creek')."

    # 3. Validate processed audio files
    processed_audio_dir = "/home/user/processed_audio"
    assert os.path.isdir(processed_audio_dir), f"Directory {processed_audio_dir} does not exist."

    for filename in data.keys():
        filepath = os.path.join(processed_audio_dir, filename)
        assert os.path.isfile(filepath), f"Audio file {filepath} referenced in API response does not exist."

        # Verify MD5 hash
        with open(filepath, "rb") as f:
            file_bytes = f.read()
            actual_md5 = hashlib.md5(file_bytes).hexdigest()

        expected_filename = f"field_record_{actual_md5}.wav"
        assert filename == expected_filename, f"Filename '{filename}' does not match its actual MD5 hash. Expected '{expected_filename}'."

        # Verify audio properties (16kHz, mono)
        try:
            with wave.open(filepath, "rb") as wav_file:
                channels = wav_file.getnchannels()
                framerate = wav_file.getframerate()

                assert channels == 1, f"Audio file {filename} is not mono (channels={channels})."
                assert framerate == 16000, f"Audio file {filename} does not have a 16kHz sample rate (framerate={framerate})."
        except wave.Error as e:
            pytest.fail(f"Failed to read {filepath} as a WAV file: {e}")