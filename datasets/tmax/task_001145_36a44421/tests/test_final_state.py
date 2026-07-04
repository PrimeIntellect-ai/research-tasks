# test_final_state.py
import os
import subprocess
import random
import tempfile
import hashlib
import pytest

def test_frames_extracted():
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Directory missing: {frames_dir}"

    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    assert len(frames) > 0, "No frames extracted"

    # Check naming convention
    for i, frame in enumerate(frames, start=1):
        expected_name = f"frame_{i:03d}.png"
        assert frame == expected_name, f"Expected frame name {expected_name}, got {frame}"

def test_frames_manifest():
    manifest_path = "/home/user/frames_manifest.txt"
    frames_dir = "/home/user/frames"
    assert os.path.isfile(manifest_path), f"Manifest missing: {manifest_path}"

    with open(manifest_path, "r") as f:
        lines = f.read().strip().split("\n")

    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
    assert len(lines) == len(frames), "Manifest line count does not match frame count"

    for line in lines:
        parts = line.split()
        assert len(parts) == 2, f"Malformed manifest line: {line}"
        hash_val, filename = parts

        frame_path = os.path.join(frames_dir, filename)
        assert os.path.isfile(frame_path), f"File in manifest not found: {filename}"

        with open(frame_path, "rb") as frame_file:
            actual_hash = hashlib.sha256(frame_file.read()).hexdigest()

        assert hash_val == actual_hash, f"Hash mismatch for {filename}"

def test_filtered_docs():
    raw_dir = "/home/user/docs_raw"
    filtered_dir = "/home/user/filtered_docs"

    assert os.path.isdir(filtered_dir), f"Directory missing: {filtered_dir}"

    raw_files = [f for f in os.listdir(raw_dir) if f.endswith(".md")]
    expected_files = []
    for f in raw_files:
        if os.path.getsize(os.path.join(raw_dir, f)) > 512:
            expected_files.append(f)

    filtered_files = [f for f in os.listdir(filtered_dir) if f.endswith(".md")]

    assert sorted(filtered_files) == sorted(expected_files), "Filtered docs do not match expected files > 512 bytes"

    for f in expected_files:
        raw_path = os.path.join(raw_dir, f)
        filtered_path = os.path.join(filtered_dir, f)

        with open(raw_path, "rb") as f1, open(filtered_path, "rb") as f2:
            assert f1.read() == f2.read(), f"Content mismatch for {f}"

def test_tdoc_parser_fuzz_equivalence():
    agent_bin = "/home/user/tdoc_parser"
    oracle_bin = "/app/oracle_tdoc_parser"

    assert os.path.isfile(agent_bin), f"Agent binary missing: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"

    assert os.path.isfile(oracle_bin), f"Oracle binary missing: {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable: {oracle_bin}"

    random.seed(42)
    iterations = 5000

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        for i in range(iterations):
            length = random.randint(0, 4096)

            # Generate interesting test cases
            case_type = random.random()
            if case_type < 0.1:
                # Valid header, random body
                data = b"TDOC\x01" + random.randbytes(max(0, length - 5))
            elif case_type < 0.2:
                # Truncated header
                data = b"TDOC\x01"[:random.randint(0, 4)]
            elif case_type < 0.3:
                # Invalid version
                data = b"TDOC\x02" + random.randbytes(max(0, length - 5))
            else:
                # Completely random
                data = random.randbytes(length)

            with open(tmp_path, "wb") as f:
                f.write(data)

            agent_res = subprocess.run([agent_bin, tmp_path], capture_output=True)
            oracle_res = subprocess.run([oracle_bin, tmp_path], capture_output=True)

            assert agent_res.returncode == oracle_res.returncode, f"Return code mismatch on iteration {i}. Oracle: {oracle_res.returncode}, Agent: {agent_res.returncode}. Input data (hex): {data.hex()}"
            assert agent_res.stdout == oracle_res.stdout, f"Stdout mismatch on iteration {i}. Oracle: {oracle_res.stdout}, Agent: {agent_res.stdout}. Input data (hex): {data.hex()}"

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)