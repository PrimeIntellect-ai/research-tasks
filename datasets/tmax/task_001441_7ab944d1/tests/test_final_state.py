# test_final_state.py

import os
import subprocess
import wave
import random
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_SCRIPT = "/home/user/audio_service/fixed_processor.py"
NUM_TESTS = 50
SAMPLE_RATE = 16000
DURATION_SEC = 1
NUM_SAMPLES = SAMPLE_RATE * DURATION_SEC

def generate_random_wav(filepath, seed):
    rng = random.Random(seed)
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)

        # Generate random 16-bit PCM samples
        samples = [rng.randint(-32768, 32767) for _ in range(NUM_SAMPLES)]

        # Pack samples into bytes
        import struct
        data = struct.pack(f"<{NUM_SAMPLES}h", *samples)
        wav_file.writeframes(data)

def test_fixed_processor_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle program not found at {ORACLE_PATH}"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(NUM_TESTS):
            input_wav = os.path.join(tmpdir, f"input_{i}.wav")
            oracle_out = os.path.join(tmpdir, f"oracle_out_{i}.wav")
            agent_out = os.path.join(tmpdir, f"agent_out_{i}.wav")

            # Generate fuzz input
            generate_random_wav(input_wav, seed=42 + i)

            # Run oracle
            oracle_cmd = [ORACLE_PATH, input_wav, oracle_out]
            oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i}:\n{oracle_proc.stderr}"
            assert os.path.isfile(oracle_out), f"Oracle did not produce output for input {i}"

            # Run agent
            agent_cmd = ["python3", AGENT_SCRIPT, input_wav, agent_out]
            agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
            assert agent_proc.returncode == 0, f"Agent script failed on input {i}:\n{agent_proc.stderr}"
            assert os.path.isfile(agent_out), f"Agent script did not produce output for input {i}"

            # Compare outputs
            with open(oracle_out, "rb") as f_oracle, open(agent_out, "rb") as f_agent:
                oracle_data = f_oracle.read()
                agent_data = f_agent.read()

            if oracle_data != agent_data:
                pytest.fail(
                    f"Mismatch on fuzz input {i}.\n"
                    f"Input WAV generated with seed {42 + i}.\n"
                    f"Oracle output size: {len(oracle_data)} bytes.\n"
                    f"Agent output size: {len(agent_data)} bytes.\n"
                    f"Outputs are not bit-exact equivalent."
                )