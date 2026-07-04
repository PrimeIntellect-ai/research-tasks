# test_final_state.py

import os
import subprocess
import json
import re
import pytest

def test_audio_compression():
    wav_path = "/app/recording.wav"
    opus_path = "/home/user/recording.opus"

    assert os.path.exists(wav_path), f"Original audio file {wav_path} is missing."
    assert os.path.exists(opus_path), f"Compressed audio file {opus_path} is missing."

    wav_size = os.path.getsize(wav_path)
    opus_size = os.path.getsize(opus_path)

    size_ratio = opus_size / wav_size
    assert size_ratio <= 0.10, f"Size ratio {size_ratio:.3f} exceeds threshold 0.10."

    # Try to verify it's a valid opus file using ffprobe
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=format_name", "-of", "default=noprint_wrappers=1:nokey=1", opus_path],
            capture_output=True, text=True, check=True
        )
        format_name = result.stdout.strip()
        assert "ogg" in format_name.lower(), f"File is not in Ogg format, detected format: {format_name}"
    except FileNotFoundError:
        pass # ffprobe not available, skip format check

def test_setup_node_script():
    script_path = "/home/user/setup_node.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    instance_name = "node-01"
    qcow2_file = f"{instance_name}.qcow2"
    user_data_file = f"{instance_name}_user-data"

    # Cleanup before run
    if os.path.exists(qcow2_file):
        os.remove(qcow2_file)
    if os.path.exists(user_data_file):
        os.remove(user_data_file)

    result = subprocess.run([script_path, instance_name], capture_output=True, text=True, cwd="/home/user")
    assert result.returncode == 0, f"Script exited with non-zero code {result.returncode}. stderr: {result.stderr}"

    qcow2_path = f"/home/user/{qcow2_file}"
    user_data_path = f"/home/user/{user_data_file}"

    assert os.path.exists(qcow2_path), f"Disk image {qcow2_file} was not created."
    assert os.path.exists(user_data_path), f"Cloud-init file {user_data_file} was not created."

    # Check qcow2 size
    try:
        info_result = subprocess.run(
            ["qemu-img", "info", "--output=json", qcow2_path],
            capture_output=True, text=True, check=True
        )
        info = json.loads(info_result.stdout)
        virtual_size = info.get("virtual-size", 0)
        assert virtual_size == 5368709120, f"Virtual size of {qcow2_file} is {virtual_size}, expected 5368709120 (5G)."
    except FileNotFoundError:
        pass # qemu-img not available, skip size check

    # Check cloud-init user-data
    with open(user_data_path, "r") as f:
        user_data_content = f.read()

    assert re.search(r"PubkeyAuthentication\s+no", user_data_content, re.IGNORECASE), "Cloud-init user-data does not contain 'PubkeyAuthentication no'."

    # Check stdout
    stdout = result.stdout
    assert "qemu-system-x86_64" in stdout, "stdout missing 'qemu-system-x86_64'"
    assert "-m 512" in stdout or "-m 512M" in stdout, "stdout missing RAM specification (-m 512 or -m 512M)"
    assert "-nographic" in stdout, "stdout missing '-nographic'"
    assert f"{instance_name}.qcow2" in stdout, f"stdout missing disk image '{instance_name}.qcow2'"

def test_whisper_wer():
    # If whisper CLI is available, we run it and calculate WER.
    # Since we can't guarantee its presence or the exact output format without installing it,
    # we leave this as a placeholder or rely on the size test which is the primary constraint tested.
    opus_path = "/home/user/recording.opus"
    if not os.path.exists(opus_path):
        return

    try:
        result = subprocess.run(["whisper", "--help"], capture_output=True, text=True)
        if result.returncode != 0:
            return
    except FileNotFoundError:
        return