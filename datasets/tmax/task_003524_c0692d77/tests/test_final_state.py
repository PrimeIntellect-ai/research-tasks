# test_final_state.py
import os
import tarfile
import pytest
from scipy.io import wavfile

def test_final_storage_archive():
    archive_path = "/home/user/final_storage.tar.gz"
    assert os.path.isfile(archive_path), f"Missing final archive: {archive_path}"

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        assert any(n.endswith("optimized.wav") for n in names), "optimized.wav not found in final_storage.tar.gz"
        assert any(n.endswith("settings.ini") for n in names), "settings.ini not found in final_storage.tar.gz"

def test_optimized_wav_size_and_validity():
    optimized_path = "/home/user/optimized.wav"
    original_path = "/app/voicemail.wav"

    assert os.path.isfile(optimized_path), f"Missing optimized file: {optimized_path}"

    original_size = os.path.getsize(original_path)
    new_size = os.path.getsize(optimized_path)
    size_ratio = new_size / original_size

    assert size_ratio <= 0.70, f"Not enough space saved. Size ratio: {size_ratio:.3f} (must be <= 0.70)"

    try:
        sample_rate, data = wavfile.read(optimized_path)
    except Exception as e:
        pytest.fail(f"Could not read optimized.wav as a valid WAV file: {e}")

    assert len(data) > 0, "Optimized WAV file contains no audio data"
    assert sample_rate > 0, "Invalid sample rate in optimized WAV file"