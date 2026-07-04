# test_final_state.py

import os
import json
import subprocess
import pytest

OUTPUT_MP3 = "/home/user/archived_call_001.mp3"
SEGMENTS_FILE = "/app/call_001_segments.txt"

def get_expected_duration():
    """Calculate the total duration of SPEECH segments."""
    duration = 0.0
    with open(SEGMENTS_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3 and parts[2] == 'SPEECH':
                duration += float(parts[1]) - float(parts[0])
    return duration

def get_media_info(file_path):
    """Use ffprobe to get media properties."""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        pytest.fail(f"ffprobe failed to read {file_path}")
    return json.loads(result.stdout)

def test_output_file_exists_and_size():
    """Test that the output MP3 exists and is within the size limit."""
    assert os.path.exists(OUTPUT_MP3), f"Output file {OUTPUT_MP3} is missing."
    assert os.path.isfile(OUTPUT_MP3), f"Expected {OUTPUT_MP3} to be a file."

    file_size = os.path.getsize(OUTPUT_MP3)
    assert file_size <= 500000, f"File size {file_size} bytes exceeds the limit of 500000 bytes."
    assert file_size > 0, "Output file is empty."

def test_output_audio_properties():
    """Test that the output MP3 has the correct format, sample rate, channels, and duration."""
    assert os.path.exists(OUTPUT_MP3), f"Output file {OUTPUT_MP3} is missing."

    info = get_media_info(OUTPUT_MP3)
    streams = info.get('streams', [])
    assert len(streams) > 0, "No audio streams found in the output file."

    audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), None)
    assert audio_stream is not None, "No audio stream found in the output file."

    # Check codec
    codec_name = audio_stream.get('codec_name')
    assert codec_name == 'mp3', f"Expected codec 'mp3', got '{codec_name}'."

    # Check sample rate
    sample_rate = audio_stream.get('sample_rate')
    assert sample_rate == '16000', f"Expected sample rate 16000 Hz, got {sample_rate} Hz."

    # Check channels (mono)
    channels = audio_stream.get('channels')
    assert channels == 1, f"Expected 1 channel (mono), got {channels} channels."

    # Check bit rate (around 32kbps)
    bit_rate = int(audio_stream.get('bit_rate', info.get('format', {}).get('bit_rate', 0)))
    # Allow some tolerance for bit rate reporting
    assert 30000 <= bit_rate <= 34000, f"Expected bit rate around 32000 bps, got {bit_rate} bps."

    # Check duration
    expected_duration = get_expected_duration()
    actual_duration = float(info.get('format', {}).get('duration', 0.0))

    # Allow a small tolerance (e.g., 1 second) for merging and compression artifacts
    duration_diff = abs(actual_duration - expected_duration)
    assert duration_diff <= 1.0, f"Expected duration ~{expected_duration:.2f}s, got {actual_duration:.2f}s. Ensure only SPEECH segments were included."