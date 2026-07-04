# test_final_state.py

import os
import subprocess
import wave
import random
import struct
import tempfile
import pytest

ORACLE_PATH = "/app/hidden/oracle_processor.sh"
AGENT_PATH = "/home/user/fixed_processor.sh"
NUM_FUZZ_TESTS = 50

def generate_random_wav(filename, duration, sample_rate, volume_multiplier):
    """Generates a random WAV file with the given parameters."""
    num_samples = int(duration * sample_rate)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        # Generate random audio data
        for _ in range(num_samples):
            # Random value between -32767 and 32767, scaled by volume
            val = int((random.random() * 2 - 1) * 32767 * volume_multiplier)
            # Clamp value
            val = max(-32768, min(32767, val))
            data = struct.pack('<h', val)
            wav_file.writeframesraw(data)

@pytest.fixture(scope="session", autouse=True)
def setup_seed():
    random.seed(42)

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Agent's script not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent's script at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle script missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle script at {ORACLE_PATH} is not executable"

    sample_rates = [8000, 16000, 22050, 44100, 48000]

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(NUM_FUZZ_TESTS):
            duration = random.uniform(1.0, 10.0)
            sample_rate = random.choice(sample_rates)
            volume_multiplier = random.uniform(0.1, 1.0)

            wav_path = os.path.join(temp_dir, f"fuzz_{i}.wav")
            generate_random_wav(wav_path, duration, sample_rate, volume_multiplier)

            # Run Oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, wav_path],
                capture_output=True,
                text=True
            )

            # Run Agent
            agent_proc = subprocess.run(
                [AGENT_PATH, wav_path],
                capture_output=True,
                text=True
            )

            # Check for crash or failure in agent
            assert agent_proc.returncode == oracle_proc.returncode, \
                f"Agent exit code ({agent_proc.returncode}) differs from oracle ({oracle_proc.returncode}) on input {wav_path}"

            # Check bit-exact equivalence of stdout
            assert agent_proc.stdout == oracle_proc.stdout, \
                f"Agent output differs from oracle on input {wav_path}.\n\nOracle output:\n{oracle_proc.stdout}\n\nAgent output:\n{agent_proc.stdout}"