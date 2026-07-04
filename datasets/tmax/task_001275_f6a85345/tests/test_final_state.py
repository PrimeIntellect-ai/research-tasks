# test_final_state.py

import os
import stat
import subprocess
import random
import zlib
import struct
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    length = random.randint(1024, 1024 * 1024)
    data = bytearray(os.urandom(length))

    # Inject some valid and invalid blocks
    num_blocks = random.randint(5, 20)
    for _ in range(num_blocks):
        pos = random.randint(0, length - 1000)
        # Magic
        data[pos] = 0x41
        data[pos+1] = 0x52

        is_valid = random.choice([True, False])
        if is_valid:
            payload = f"/fake/path/file_{random.randint(1, 1000)}.txt".encode()
            comp = zlib.compress(payload)
            comp_len = len(comp)
            data[pos+2:pos+6] = struct.pack("<I", comp_len)
            if pos + 6 + comp_len < length:
                data[pos+6:pos+6+comp_len] = comp
        else:
            comp_len = random.randint(1, 500)
            data[pos+2:pos+6] = struct.pack("<I", comp_len)
            # Leave random data as corrupted zlib

    return bytes(data)

def test_extractor_fuzz_equivalence():
    agent_bin = "/home/user/extractor"
    oracle_bin = "/app/oracle_extractor"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"

    for i in range(100):
        fuzz_data = generate_fuzz_input(i)

        oracle_proc = subprocess.run(
            [oracle_bin], input=fuzz_data, capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_bin], input=fuzz_data, capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on fuzz iteration {i}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Stdout mismatch on fuzz iteration {i}"

def test_curation_and_links():
    manifest_path = "/home/user/final_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest not found at {manifest_path}"

    with open(manifest_path, "r") as f:
        manifest_lines = [line.strip() for line in f if line.strip()]

    # Find matching files in /app/incoming
    incoming_dir = "/app/incoming"
    matching_files = []
    for root, dirs, files in os.walk(incoming_dir):
        for file in files:
            full_path = os.path.join(root, file)
            st = os.stat(full_path)
            if st.st_size > 1024 and (st.st_mode & stat.S_ISUID):
                matching_files.append(full_path)

    # Extract expected paths using oracle
    expected_paths = []
    for mf in matching_files:
        with open(mf, "rb") as f:
            data = f.read()
        proc = subprocess.run(["/app/oracle_extractor"], input=data, capture_output=True, text=True)
        expected_paths.extend([line.strip() for line in proc.stdout.splitlines() if line.strip()])

    assert set(manifest_lines) == set(expected_paths), "Manifest contents do not match expected extracted paths"

    if not expected_paths:
        return

    # Check links
    latest_link = "/home/user/latest_artifact"
    assert os.path.islink(latest_link), f"{latest_link} is not a symlink"

    # Find most recently modified file among expected_paths
    existing_paths = [p for p in expected_paths if os.path.exists(p)]
    if existing_paths:
        latest_file = max(existing_paths, key=lambda p: os.stat(p).st_mtime)
        assert os.readlink(latest_link) == latest_file, f"Symlink does not point to the latest file: {latest_file}"

        curated_dir = "/home/user/curated_archive"
        assert os.path.isdir(curated_dir), f"Curated archive directory not found at {curated_dir}"

        for p in existing_paths:
            if p == latest_file:
                continue
            basename = os.path.basename(p)
            hardlink_path = os.path.join(curated_dir, basename)
            assert os.path.isfile(hardlink_path), f"Hard link not found for {basename}"
            assert os.stat(hardlink_path).st_ino == os.stat(p).st_ino, f"{hardlink_path} is not a hard link to {p}"