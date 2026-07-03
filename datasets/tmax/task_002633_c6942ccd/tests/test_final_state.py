# test_final_state.py

import os
import json
import hashlib
import random
import struct
import string
import subprocess
import pytest

def test_part1_frames_and_manifest():
    frames_dir = "/home/user/frames"
    manifest_path = "/home/user/manifest.json"

    assert os.path.isdir(frames_dir), f"{frames_dir} is not a directory"
    frames = sorted(f for f in os.listdir(frames_dir) if f.endswith('.jpg'))
    assert len(frames) == 15, f"Expected 15 jpg frames, found {len(frames)}"

    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist"
    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON")

    for frame in frames:
        frame_path = os.path.join(frames_dir, frame)
        with open(frame_path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        assert frame in manifest, f"Frame {frame} missing from manifest"
        assert manifest[frame] == h, f"Hash mismatch for {frame}: expected {h}, got {manifest[frame]}"

def generate_varc(seed):
    random.seed(seed)

    if random.random() < 0.1:
        magic = b"VBRC"
    else:
        magic = b"VARC"

    data = bytearray(magic)

    entry_count = random.randint(0, 50)
    data += struct.pack(">H", entry_count)

    for _ in range(entry_count):
        path_len = random.randint(1, 255)
        chars = string.ascii_letters + string.digits + "/._-"
        path = "".join(random.choices(chars, k=path_len))

        if random.random() < 0.3:
            malicious = random.choice(["../", "../../", "/absolute/path"])
            insert_pos = random.randint(0, len(path))
            path = path[:insert_pos] + malicious + path[insert_pos:]

        path_bytes = path.encode('utf-8')[:65535]
        data += struct.pack(">H", len(path_bytes))
        data += path_bytes

        data_len = random.randint(0, 10000)
        data += struct.pack(">I", data_len)
        data += bytes(random.choices(range(256), k=data_len))

    if random.random() < 0.2:
        if len(data) > 0:
            trunc_len = random.randint(0, len(data) - 1)
            data = data[:trunc_len]

    return bytes(data)

def test_part2_fuzz_equivalence():
    agent_script = "/home/user/parse_archive.py"
    assert os.path.isfile(agent_script), f"{agent_script} does not exist"
    oracle_script = "/app/oracle_parse_archive"
    assert os.path.isfile(oracle_script), f"Oracle {oracle_script} does not exist"

    for i in range(1000):
        test_data = generate_varc(i)

        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=test_data,
            capture_output=True
        )

        oracle_proc = subprocess.run(
            [oracle_script],
            input=test_data,
            capture_output=True
        )

        if agent_proc.returncode != oracle_proc.returncode:
            pytest.fail(f"Exit code mismatch on input seed {i}.\nOracle exit code: {oracle_proc.returncode}\nAgent exit code: {agent_proc.returncode}\nOracle stdout: {oracle_proc.stdout}\nAgent stdout: {agent_proc.stdout}")

        if agent_proc.stdout != oracle_proc.stdout:
            pytest.fail(f"Stdout mismatch on input seed {i}.\nOracle stdout:\n{oracle_proc.stdout.decode('utf-8', errors='replace')}\nAgent stdout:\n{agent_proc.stdout.decode('utf-8', errors='replace')}")