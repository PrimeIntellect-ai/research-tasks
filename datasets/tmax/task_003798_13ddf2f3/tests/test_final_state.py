# test_final_state.py

import os
import subprocess
import random
import pytest

def test_raw_audio_extraction():
    """Verify that raw_audio.bin is correctly extracted from telemetry.wav."""
    raw_audio_path = "/home/user/raw_audio.bin"
    assert os.path.exists(raw_audio_path), f"Missing file: {raw_audio_path}"

    # Recompute the expected raw_audio.bin
    expected_raw_audio_path = "/tmp/expected_raw_audio.bin"
    subprocess.run([
        "ffmpeg", "-y", "-i", "/app/telemetry.wav", 
        "-f", "u8", "-acodec", "pcm_u8", expected_raw_audio_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(raw_audio_path, "rb") as f1, open(expected_raw_audio_path, "rb") as f2:
        assert f1.read() == f2.read(), "The contents of raw_audio.bin do not match the expected 8-bit unsigned PCM extraction."

def test_state_sequence_output():
    """Verify that state_sequence.bin matches the output of the oracle on raw_audio.bin."""
    state_sequence_path = "/home/user/state_sequence.bin"
    raw_audio_path = "/home/user/raw_audio.bin"
    oracle_path = "/opt/oracle/bayesian_filter_reference"

    assert os.path.exists(state_sequence_path), f"Missing file: {state_sequence_path}"
    assert os.path.exists(raw_audio_path), f"Missing file: {raw_audio_path}"
    assert os.path.exists(oracle_path), f"Missing oracle: {oracle_path}"

    with open(raw_audio_path, "rb") as f_in:
        raw_audio_data = f_in.read()

    result = subprocess.run([oracle_path], input=raw_audio_data, capture_output=True, check=True)
    expected_output = result.stdout

    with open(state_sequence_path, "rb") as f_out:
        actual_output = f_out.read()

    assert actual_output == expected_output, "The contents of state_sequence.bin do not match the expected output from the Bayesian filter."

def test_fuzz_equivalence():
    """Fuzz the agent's C program against the oracle reference implementation."""
    agent_binary = "/home/user/bayesian_filter"
    oracle_binary = "/opt/oracle/bayesian_filter_reference"

    assert os.path.exists(agent_binary), f"Agent binary not found: {agent_binary}"
    assert os.access(agent_binary, os.X_OK), f"Agent binary is not executable: {agent_binary}"

    random.seed(42)
    iterations = 1000
    min_len = 1
    max_len = 50000

    for i in range(iterations):
        length = random.randint(min_len, max_len)
        test_input = bytes(random.choices(range(256), k=length))

        oracle_proc = subprocess.run([oracle_binary], input=test_input, capture_output=True)
        assert oracle_proc.returncode == 0, "Oracle binary crashed."
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run([agent_binary], input=test_input, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent binary crashed on fuzz iteration {i}."
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            # Provide a truncated view if it's too long
            display_input = test_input[:50].hex() + ("..." if len(test_input) > 50 else "")
            display_oracle = oracle_out[:50].hex() + ("..." if len(oracle_out) > 50 else "")
            display_agent = agent_out[:50].hex() + ("..." if len(agent_out) > 50 else "")

            pytest.fail(
                f"Fuzz equivalence failed on iteration {i}.\n"
                f"Input length: {length}\n"
                f"Input (hex): {display_input}\n"
                f"Expected output (hex): {display_oracle}\n"
                f"Actual output (hex): {display_agent}"
            )