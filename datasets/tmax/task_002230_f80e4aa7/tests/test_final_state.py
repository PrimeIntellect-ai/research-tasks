# test_final_state.py
import os
import subprocess
import ssl
import urllib.request
import numpy as np
from scipy.io import wavfile
import pytest

def test_deploy_script_exists():
    """Check that deploy.sh exists and is executable."""
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Deploy script {script_path} is not executable."

def test_rust_project_exists():
    """Check that the Rust project was created."""
    cargo_path = "/home/user/audiocompress/Cargo.toml"
    assert os.path.isfile(cargo_path), f"Rust project Cargo.toml missing at {cargo_path}."

def test_certs_exist():
    """Check that the TLS certificates were generated."""
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate missing at {cert_path}."
    assert os.path.isfile(key_path), f"Private key missing at {key_path}."

def test_acls_applied():
    """Check that ACLs were applied to the media directory for www-data."""
    media_dir = "/home/user/srv/media"
    assert os.path.isdir(media_dir), f"Media directory {media_dir} is missing."

    # Check directory ACL
    result = subprocess.run(["getfacl", "-c", media_dir], capture_output=True, text=True)
    assert "user:www-data:r-x" in result.stdout, "www-data does not have r-x ACL on the media directory."

def test_nginx_running():
    """Check that nginx is listening on port 4433."""
    result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
    assert ":4433" in result.stdout, "Nginx is not listening on port 4433."

def test_audio_psnr():
    """Fetch the output MP3 via HTTPS and verify the PSNR >= 20.0."""
    url = "https://127.0.0.1:4433/output.mp3"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, context=ctx) as response, open("/tmp/eval_output.mp3", "wb") as f:
            f.write(response.read())
    except Exception as e:
        pytest.fail(f"Failed to fetch {url}: {e}")

    assert os.path.isfile("/tmp/eval_output.mp3"), "Downloaded MP3 file is missing."

    # Convert to wav for comparison
    subprocess.run(["ffmpeg", "-y", "-i", "/tmp/eval_output.mp3", "-ar", "44100", "-ac", "1", "/tmp/eval_output.wav"], 
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-i", "/app/input.wav", "-ac", "1", "/tmp/eval_input_mono.wav"], 
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sr1, ref_audio = wavfile.read("/tmp/eval_input_mono.wav")
    sr2, test_audio = wavfile.read("/tmp/eval_output.wav")

    min_len = min(len(ref_audio), len(test_audio))
    ref_audio = ref_audio[:min_len].astype(np.float32)
    test_audio = test_audio[:min_len].astype(np.float32)

    mse = np.mean((ref_audio - test_audio) ** 2)
    if mse == 0:
        psnr = 100.0
    else:
        max_pixel = 32767.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))

    assert psnr >= 20.0, f"Audio quality too low, PSNR is {psnr} dB (Threshold: 20.0 dB)"