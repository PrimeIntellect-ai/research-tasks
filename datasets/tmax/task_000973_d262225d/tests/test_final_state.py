# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/pack_audio.py"
ORACLE_SCRIPT = "/opt/oracle/pack_audio_oracle.py"

def generate_random_tree(base_dir, seed):
    rng = random.Random(seed)
    num_files = rng.randint(0, 15)
    num_loops = rng.randint(0, 5)

    # Create some directories
    dirs = [base_dir]
    for _ in range(5):
        d = os.path.join(rng.choice(dirs), f"dir_{rng.randint(1000, 9999)}")
        os.makedirs(d, exist_ok=True)
        dirs.append(d)

    # Create wav files
    for _ in range(num_files):
        d = rng.choice(dirs)
        f_path = os.path.join(d, f"file_{rng.randint(1000, 9999)}.wav")
        length = rng.randint(0, 5000)
        # Generate bytes with repetition to test RLE
        content = bytearray()
        while len(content) < length:
            char = rng.choice(b"ABCDEF\x00\xff\x12\x34")
            run_len = rng.randint(1, min(300, length - len(content) + 1))
            content.extend([char] * run_len)
        content = content[:length]
        with open(f_path, "wb") as f:
            f.write(content)

    # Create symlink loops
    for _ in range(num_loops):
        src = rng.choice(dirs)
        dst = os.path.join(rng.choice(dirs), f"link_{rng.randint(1000, 9999)}")
        if not os.path.exists(dst):
            os.symlink(src, dst)

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script missing: {ORACLE_SCRIPT}"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(30):
            test_dir = os.path.join(tmpdir, f"test_{i}")
            os.makedirs(test_dir)
            generate_random_tree(test_dir, seed=42+i)

            agent_out = os.path.join(tmpdir, f"agent_{i}.car")
            oracle_out = os.path.join(tmpdir, f"oracle_{i}.car")

            # Run oracle
            subprocess.run(["python3", ORACLE_SCRIPT, "pack", test_dir, oracle_out], check=True)

            # Run agent
            res = subprocess.run(["python3", AGENT_SCRIPT, "pack", test_dir, agent_out], capture_output=True, text=True)
            assert res.returncode == 0, f"Agent failed on pack. Stderr: {res.stderr}"

            # Compare outputs
            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            assert oracle_data == agent_data, f"Mismatch on fuzz iteration {i}. Expected {len(oracle_data)} bytes, got {len(agent_data)} bytes."

            # Test verify (unmodified)
            res_verify = subprocess.run(["python3", AGENT_SCRIPT, "verify", agent_out], capture_output=True, text=True)
            assert res_verify.returncode == 0, f"Agent verify failed on unmodified archive {i}. Stderr: {res_verify.stderr}"
            assert "Archive OK" in res_verify.stdout, f"Agent verify output incorrect for OK on archive {i}"

            # Test verify (corrupted)
            if len(agent_data) > 13: # Magic header + crc size
                corrupt_out = os.path.join(tmpdir, f"corrupt_{i}.car")
                corrupt_data = bytearray(agent_data)
                # Corrupt a byte in the middle
                idx = len(corrupt_data) // 2
                corrupt_data[idx] = (corrupt_data[idx] + 1) % 256
                with open(corrupt_out, "wb") as f:
                    f.write(corrupt_data)

                res_corrupt = subprocess.run(["python3", AGENT_SCRIPT, "verify", corrupt_out], capture_output=True, text=True)
                assert res_corrupt.returncode == 1, f"Agent verify did not exit with 1 on corrupted archive {i}"
                assert "Archive Corrupted" in res_corrupt.stdout, f"Agent verify output incorrect for Corrupted on archive {i}"

def test_integration_dataset():
    dataset_car = "/home/user/dataset.car"
    assert os.path.isfile(dataset_car), f"Integration output missing: {dataset_car}"

    with tempfile.TemporaryDirectory() as tmpdir:
        oracle_out = os.path.join(tmpdir, "oracle_dataset.car")
        subprocess.run(["python3", ORACLE_SCRIPT, "pack", "/app/dataset", oracle_out], check=True)

        with open(oracle_out, "rb") as f:
            oracle_data = f.read()
        with open(dataset_car, "rb") as f:
            agent_data = f.read()

        assert oracle_data == agent_data, "Integration output /home/user/dataset.car does not match oracle output."