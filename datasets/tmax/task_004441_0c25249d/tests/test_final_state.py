# test_final_state.py

import os
import subprocess
import struct
import random
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/audio_analyzer_oracle"
AGENT_PATH = "/home/user/audio_analyzer_fixed"

def test_student_files_exist():
    assert os.path.isfile(AGENT_PATH), f"Missing compiled executable: {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Executable is not executable: {AGENT_PATH}"
    assert os.path.isfile("/home/user/test_input.bin"), "Missing /home/user/test_input.bin"
    assert os.path.isfile("/home/user/diagnostic_output.txt"), "Missing /home/user/diagnostic_output.txt"
    assert os.path.isfile("/home/user/run_regression.sh"), "Missing /home/user/run_regression.sh"

def generate_fuzz_input(seed):
    random.seed(seed)
    # Header: "DIAG" (4 bytes) + length (4 bytes) + 24 null bytes
    header_magic = b"DIAG"

    # 50% chance of 0xFFFFFFFF length
    if random.random() < 0.5:
        length_val = 0xFFFFFFFF
    else:
        length_val = random.randint(0, 50000)

    header_length = struct.pack("<I", length_val)
    header = header_magic + header_length + (b"\x00" * 24)

    # Generate data
    num_samples = length_val if length_val != 0xFFFFFFFF else random.randint(0, 50000)

    # Extreme DC offset
    dc_offset = random.choice([0, 15000, -15000, 30000, -30000])

    data = bytearray()
    for _ in range(num_samples):
        val = int(random.gauss(dc_offset, 1000))
        val = max(-32768, min(32767, val))
        data.extend(struct.pack("<h", val))

    return header + data

def test_fuzz_equivalence():
    if not os.path.isfile(ORACLE_PATH):
        pytest.skip("Oracle binary not found. Skipping fuzz equivalence test.")

    num_tests = 100

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_tests):
            input_data = generate_fuzz_input(i)
            input_path = os.path.join(tmpdir, f"input_{i}.bin")

            with open(input_path, "wb") as f:
                f.write(input_data)

            oracle_proc = subprocess.run(
                [ORACLE_PATH, input_path],
                capture_output=True,
                text=True
            )

            agent_proc = subprocess.run(
                [AGENT_PATH, input_path],
                capture_output=True,
                text=True
            )

            assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {i}"

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            assert agent_out == oracle_out, f"Output mismatch on input {i} (seed {i}).\nOracle:\n{oracle_out}\nAgent:\n{agent_out}"