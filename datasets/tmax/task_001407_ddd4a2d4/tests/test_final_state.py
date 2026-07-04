# test_final_state.py

import os
import wave
import struct
import math
import pytest

def calculate_rms(wav_path):
    with wave.open(wav_path, 'rb') as w:
        n_frames = w.getnframes()
        data = w.readframes(n_frames)
        samples = struct.unpack(f'<{n_frames}h', data)
        sq_sum = sum(s**2 for s in samples)
        return math.sqrt(sq_sum / n_frames)

def test_directories_and_symlink():
    assert os.path.isdir("/home/user/inbox"), "/home/user/inbox directory is missing"
    assert os.path.isdir("/home/user/outbox"), "/home/user/outbox directory is missing"

    symlink_path = "/home/user/inbox/target.wav"
    assert os.path.islink(symlink_path), f"Symlink missing at {symlink_path}"
    assert os.readlink(symlink_path) == "/app/input.wav", f"Symlink {symlink_path} does not point to /app/input.wav"

def test_binary_exists():
    binary_path = "/home/user/bin/analyzer"
    assert os.path.isfile(binary_path), f"Compiled binary missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_service_file_exists():
    service_path = "/home/user/.config/systemd/user/audio-analyzer.service"
    assert os.path.isfile(service_path), f"Systemd service file missing at {service_path}"

def test_health_check_files():
    script_path = "/home/user/health_check.sh"
    log_path = "/home/user/health.log"

    assert os.path.isfile(script_path), f"Health check script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Health check script at {script_path} is not executable"

    assert os.path.isfile(log_path), f"Health log missing at {log_path}"
    with open(log_path, 'r') as f:
        content = f.read()
    assert "Active:" in content, "Health log does not contain 'Active:' line"

def test_rms_value():
    output_path = "/home/user/outbox/rms.txt"
    assert os.path.isfile(output_path), f"Output file missing at {output_path}"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    try:
        agent_rms = float(content)
    except ValueError:
        pytest.fail(f"Could not parse RMS value from {output_path}: '{content}'")

    truth_rms = calculate_rms('/app/input.wav')

    error = abs(agent_rms - truth_rms)
    assert error <= 1.0, f"RMS metric error too high: expected ~{truth_rms:.2f}, got {agent_rms:.2f} (diff: {error:.2f} > 1.0)"