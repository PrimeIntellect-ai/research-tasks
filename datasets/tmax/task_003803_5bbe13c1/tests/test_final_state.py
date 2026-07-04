# test_final_state.py

import os
import subprocess
import random
import tempfile
import zlib
import struct
from pathlib import Path

def test_fuzz_equivalence():
    oracle_path = "/app/header_parser"
    agent_path = "/home/user/parse_header.sh"

    assert os.path.exists(agent_path), f"Agent script not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent script at {agent_path} is not executable"

    random.seed(42)

    # Generate 500 test cases
    for i in range(500):
        category = random.random()
        if category < 0.2:
            # 0-15 bytes
            length = random.randint(0, 15)
            data = bytes(random.getrandbits(8) for _ in range(length))
        elif category < 0.4:
            # 16-1024 bytes, bad magic
            length = random.randint(16, 1024)
            data = bytearray(random.getrandbits(8) for _ in range(length))
            # Ensure bad magic
            while data[0:4] == b"PDAT":
                data[0:4] = bytes(random.getrandbits(8) for _ in range(4))
        else:
            # 16-1024 bytes, good magic
            length = random.randint(16, 1024)
            data = bytearray(random.getrandbits(8) for _ in range(length))
            data[0:4] = b"PDAT"

            # Decide if valid CRC
            payload = data[16:]
            if len(payload) == 0:
                crc = 0
            else:
                crc = zlib.crc32(payload) & 0xFFFFFFFF

            if random.random() < 0.5:
                # Corrupt CRC
                crc ^= 0xFFFFFFFF

            struct.pack_into("<I", data, 12, crc)

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(data)
            tmp_path = f.name

        try:
            oracle_proc = subprocess.run([oracle_path, tmp_path], capture_output=True, text=True)
            agent_proc = subprocess.run([agent_path, tmp_path], capture_output=True, text=True)

            assert oracle_proc.stdout == agent_proc.stdout, f"Mismatch on input {i} (len {len(data)}).\nOracle stdout: {repr(oracle_proc.stdout)}\nAgent stdout: {repr(agent_proc.stdout)}"
            assert oracle_proc.stderr == agent_proc.stderr, f"Mismatch on input {i} (len {len(data)}).\nOracle stderr: {repr(oracle_proc.stderr)}\nAgent stderr: {repr(agent_proc.stderr)}"
        finally:
            os.remove(tmp_path)

def test_organization_state():
    raw_dir = Path("/home/user/raw_data")
    org_dir = Path("/home/user/organized_data")
    log_file = Path("/home/user/corrupt_files.log")
    oracle_path = "/app/header_parser"

    assert org_dir.exists(), f"Organized data directory not found at {org_dir}"

    expected_corrupt = set()
    expected_organized = set()

    for dat_file in raw_dir.glob("*.dat"):
        proc = subprocess.run([oracle_path, str(dat_file)], capture_output=True, text=True)
        out = proc.stdout.strip()
        if out.startswith("ERROR:") or "INTEGRITY:INVALID" in out:
            expected_corrupt.add(dat_file.name)
        else:
            # Extract TS, DEV, EXP
            # Format: TS:<timestamp> DEV:<device_id> EXP:<exp_id> INTEGRITY:VALID
            parts = out.split()
            ts = parts[0].split(":")[1]
            dev = parts[1].split(":")[1]
            exp = parts[2].split(":")[1]
            expected_path = org_dir / f"DEV_{dev}" / f"EXP_{exp}" / f"{ts}.dat"
            expected_organized.add((dat_file, expected_path))

    if expected_corrupt:
        assert log_file.exists(), "corrupt_files.log does not exist"
        with open(log_file, "r") as f:
            log_contents = f.read()
        for c in expected_corrupt:
            assert c in log_contents, f"Expected {c} to be logged in corrupt_files.log"

    for src, dst in expected_organized:
        assert dst.exists(), f"Expected organized file not found at {dst}"
        with open(src, "rb") as f1, open(dst, "rb") as f2:
            assert f1.read() == f2.read(), f"File content mismatch for {dst}"