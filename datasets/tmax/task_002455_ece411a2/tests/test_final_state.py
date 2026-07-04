# test_final_state.py

import os
import subprocess
import random
import wave
import struct
import math
import tempfile

def generate_random_wav(filepath, num_samples):
    """Generate a valid 16-bit Mono PCM WAV file at 8000Hz with random noise and sine waves."""
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(8000)

        # Mix of sine sweep and noise
        freq_start = random.uniform(100, 500)
        freq_end = random.uniform(500, 2000)
        noise_level = random.uniform(0.1, 0.5)

        data = bytearray(num_samples * 2)
        for i in range(num_samples):
            t = i / 8000.0
            # Linear frequency sweep
            current_freq = freq_start + (freq_end - freq_start) * (i / num_samples)
            sine_val = math.sin(2 * math.pi * current_freq * t)

            # Noise
            noise_val = random.uniform(-1.0, 1.0)

            # Combine
            val = sine_val * (1 - noise_level) + noise_val * noise_level

            # Scale to 16-bit range (-32768 to 32767)
            int_val = int(val * 32767)
            int_val = max(-32768, min(32767, int_val))

            struct.pack_into('<h', data, i * 2, int_val)

        wav_file.writeframes(data)

def test_fuzz_equivalence():
    oracle_cmd = ["/app/legacy_detector"]
    agent_cmd = ["python3", "/home/user/detector.py"]

    assert os.path.isfile(oracle_cmd[0]), f"Oracle program missing: {oracle_cmd[0]}"
    assert os.path.isfile(agent_cmd[1]), f"Agent program missing: {agent_cmd[1]}"

    random.seed(42)
    num_iterations = 100

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(num_iterations):
            num_samples = random.randint(1000, 100000)
            wav_path = os.path.join(temp_dir, f"test_{i}.wav")
            generate_random_wav(wav_path, num_samples)

            # Run oracle
            try:
                oracle_result = subprocess.run(
                    oracle_cmd + [wav_path],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
            except subprocess.CalledProcessError as e:
                assert False, f"Oracle failed on input {wav_path}. Stderr: {e.stderr}"
            except subprocess.TimeoutExpired:
                assert False, f"Oracle timed out on input {wav_path}."

            # Run agent
            try:
                agent_result = subprocess.run(
                    agent_cmd + [wav_path],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
            except subprocess.CalledProcessError as e:
                assert False, f"Agent program failed on input {wav_path}. Stderr: {e.stderr}"
            except subprocess.TimeoutExpired:
                assert False, f"Agent program timed out on input {wav_path}."

            oracle_output = oracle_result.stdout.strip()
            agent_output = agent_result.stdout.strip()

            assert oracle_output == agent_output, (
                f"Mismatch on fuzz iteration {i} (samples: {num_samples}).\n"
                f"Oracle output starts with: {oracle_output[:100]}...\n"
                f"Agent output starts with: {agent_output[:100]}...\n"
            )