# test_final_state.py

import os
import glob
import urllib.request
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import pytest

def test_symlinks_created():
    """Test that symbolic links for all .log and .wav files are created in the backup_view directory."""
    raw_dir = '/app/restored_data/raw'
    backup_dir = '/home/user/backup_view'

    assert os.path.isdir(backup_dir), f"Directory missing: {backup_dir}"

    # Find all .log and .wav files in raw_dir
    raw_files = []
    for ext in ('*.log', '*.wav'):
        raw_files.extend(glob.glob(f'{raw_dir}/**/{ext}', recursive=True))

    assert len(raw_files) > 0, "No raw files found to test symlinks."

    for f in raw_files:
        basename = os.path.basename(f)
        link_path = os.path.join(backup_dir, basename)
        assert os.path.islink(link_path), f"Expected symlink at {link_path}"
        assert os.path.realpath(link_path) == os.path.realpath(f), f"Symlink {link_path} does not point to {f}"

def test_audio_compression_metrics():
    """Test that the compressed audio file meets size and MSE constraints."""
    orig_file = '/app/restored_data/raw/incidents/audio/alert_001.wav'
    comp_file = '/home/user/backup_view/alert_001_compressed.wav'

    assert os.path.isfile(orig_file), f"Original file missing: {orig_file}"
    assert os.path.isfile(comp_file), f"Compressed file missing: {comp_file}"

    # Check file size reduction
    orig_size = os.path.getsize(orig_file)
    comp_size = os.path.getsize(comp_file)
    max_allowed_size = 0.7 * orig_size
    assert comp_size <= max_allowed_size, f"Compressed file size ({comp_size} bytes) is not <= 70% of original ({max_allowed_size} bytes)"

    # Check MSE
    rate_orig, data_orig = wavfile.read(orig_file)
    rate_comp, data_comp = wavfile.read(comp_file)

    # Align arrays if lengths differ (e.g., due to downsampling)
    if len(data_orig) != len(data_comp):
        data_comp_aligned = resample(data_comp, len(data_orig))
    else:
        data_comp_aligned = data_comp

    # Compute Mean Squared Error
    mse = np.mean((data_orig.astype(float) - data_comp_aligned.astype(float))**2)
    assert mse <= 5000, f"MSE {mse:.2f} exceeds the maximum allowed threshold of 5000"

def test_reverse_proxy():
    """Test that the reverse proxy is running on port 8080 and serving the compressed file."""
    comp_file = '/home/user/backup_view/alert_001_compressed.wav'
    assert os.path.isfile(comp_file), f"Compressed file missing: {comp_file}"

    url = "http://localhost:8080/alert_001_compressed.wav"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        assert req.status == 200, f"Expected HTTP status 200, got {req.status}"
        content = req.read()
    except Exception as e:
        pytest.fail(f"Failed to fetch file via reverse proxy at {url}: {e}")

    with open(comp_file, 'rb') as f:
        expected_content = f.read()

    assert content == expected_content, "Content served by proxy does not match the actual compressed file."