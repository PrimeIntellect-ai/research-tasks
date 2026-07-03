# test_final_state.py

import os
import re
import subprocess
import pytest

def test_auth_exp_behavior():
    path = "/home/user/auth.exp"
    assert os.path.exists(path), f"Expect script {path} does not exist."
    assert os.access(path, os.X_OK), f"Expect script {path} is not executable."

    result = subprocess.run([path], capture_output=True, text=True)
    output = result.stdout.strip()
    # The requirement says it prints ONLY the final token.
    # Depending on expect's log_user settings, it might output other things, 
    # but it must at least contain the token and ideally be just the token.
    assert "TOKEN_99AABBCC" in output, f"auth.exp did not output the correct token. Output was: {output}"

def test_fstab_staged_content():
    path = "/home/user/fstab.staged"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    assert len(lines) == 1, f"Expected exactly 1 active line in {path}, found {len(lines)}."

    parts = lines[0].split()
    assert len(parts) == 6, f"Expected 6 fields in fstab line, found {len(parts)}."

    assert parts[0] == "10.0.5.50:/var/video_archive", f"Incorrect device/share: {parts[0]}"
    assert parts[1] == "/mnt/video_staged", f"Incorrect mount point: {parts[1]}"
    assert parts[2] == "nfs4", f"Incorrect filesystem type: {parts[2]}"

    opts = parts[3].split(",")
    expected_opts = ["rw", "soft", "intr", "noatime", "x-systemd.automount"]
    for opt in expected_opts:
        assert opt in opts, f"Missing mount option '{opt}' in {parts[3]}."

    assert parts[4] == "0", f"Incorrect dump value: {parts[4]}"
    assert parts[5] == "0", f"Incorrect pass value: {parts[5]}"

def test_optimize_stream_script_exists():
    path = "/home/user/optimize_stream.sh"
    assert os.path.exists(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
    assert "AUTH_TOKEN" in content, "Variable AUTH_TOKEN not assigned in optimize_stream.sh."

def test_video_ssim_metric():
    source = "/app/traffic_cam.mp4"
    output = "/home/user/migrated_stream.mp4"

    assert os.path.exists(output), f"Output video {output} does not exist."
    assert os.path.getsize(output) > 0, f"Output video {output} is empty (0 bytes)."

    cmd = [
        "ffmpeg", "-i", source, "-i", output,
        "-lavfi", "ssim", "-f", "null", "-"
    ]

    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    match = re.search(r"All:([0-9.]+)", result.stderr)

    assert match is not None, "Could not parse SSIM metric from ffmpeg output."

    ssim_val = float(match.group(1))
    assert ssim_val >= 0.90, f"SSIM value {ssim_val} is less than the required threshold of 0.90."

def test_systemd_service_content():
    path = "/home/user/.config/systemd/user/video-migrator.service"
    assert os.path.exists(path), f"Systemd service file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "ExecStart=/home/user/optimize_stream.sh" in content, "ExecStart is incorrect or missing in service file."
    assert "Type=oneshot" in content, "Type=oneshot is missing in service file."
    assert "WantedBy=default.target" in content, "WantedBy=default.target is missing in service file."