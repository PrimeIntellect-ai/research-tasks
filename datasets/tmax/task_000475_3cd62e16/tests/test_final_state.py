# test_final_state.py

import os
import subprocess
import tempfile
import wave
import random
import shutil
import pytest

ORACLE_PATH = "/app/ref_filter.py"
AGENT_PATH = "/home/user/audio_filter_fixed"
NUM_TESTS = 50

def create_random_wav(path, duration_sec):
    sample_rate = 44100
    num_samples = int(sample_rate * duration_sec)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(os.urandom(num_samples * 2))

@pytest.fixture(scope="module")
def setup_env():
    assert os.path.isfile(AGENT_PATH), f"Agent executable missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable is not executable: {AGENT_PATH}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

def test_fuzz_equivalence_and_memory_leak(setup_env):
    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(NUM_TESTS):
            duration = random.uniform(1.0, 10.0)
            input_wav = os.path.join(tmpdir, f"input_{i}.wav")
            oracle_out = os.path.join(tmpdir, f"oracle_out_{i}.bin")
            agent_out = os.path.join(tmpdir, f"agent_out_{i}.bin")

            create_random_wav(input_wav, duration)

            # Run oracle
            oracle_cmd = ["python3", ORACLE_PATH, input_wav, oracle_out]
            try:
                subprocess.run(oracle_cmd, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on input {input_wav}:\n{e.stderr}")

            # Run agent under valgrind for a few tests to save time, but at least test memory leak
            # We'll run valgrind on the first 5 tests
            if i < 5:
                valgrind_cmd = [
                    "valgrind",
                    "--leak-check=full",
                    "--error-exitcode=1",
                    AGENT_PATH,
                    input_wav,
                    agent_out
                ]
                try:
                    res = subprocess.run(valgrind_cmd, check=True, capture_output=True, text=True)
                    assert "definitely lost: 0 bytes" in res.stderr, f"Memory leak detected in {AGENT_PATH} on input {input_wav}:\n{res.stderr}"
                except subprocess.CalledProcessError as e:
                    pytest.fail(f"Agent failed or leaked memory on input {input_wav}:\n{e.stderr}")
            else:
                agent_cmd = [AGENT_PATH, input_wav, agent_out]
                try:
                    subprocess.run(agent_cmd, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    pytest.fail(f"Agent failed on input {input_wav}:\n{e.stderr}")

            # Compare outputs
            assert os.path.isfile(oracle_out), f"Oracle output missing for {input_wav}"
            assert os.path.isfile(agent_out), f"Agent output missing for {input_wav}"

            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            if oracle_data != agent_data:
                pytest.fail(f"Output mismatch on random input {i} (duration: {duration:.2f}s).\n"
                            f"Oracle output size: {len(oracle_data)}\n"
                            f"Agent output size: {len(agent_data)}\n"
                            "Floating-point precision loss or algorithmic error is likely present.")