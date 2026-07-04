# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile

def test_rust_parser_exists():
    assert os.path.exists("/home/user/parser.rs"), "The Rust parser file /home/user/parser.rs is missing."

def test_optimized_memo_audio_metric():
    agent_file = "/home/user/optimized_memo.wav"
    reference_file = "/tmp/reference_memo.wav"

    assert os.path.exists(agent_file), f"Agent file not found at {agent_file}"
    assert os.path.exists(reference_file), f"Reference file not found at {reference_file}"

    try:
        rate_ref, data_ref = wavfile.read(reference_file)
    except Exception as e:
        assert False, f"Failed to read reference WAV file: {e}"

    try:
        rate_agent, data_agent = wavfile.read(agent_file)
    except Exception as e:
        assert False, f"Failed to read agent WAV file: {e}"

    assert rate_ref == rate_agent, f"Sample rate mismatch: reference is {rate_ref}, agent is {rate_agent}"

    # Ensure mono for simplicity in comparison
    if len(data_ref.shape) > 1:
        data_ref = data_ref[:, 0]
    if len(data_agent.shape) > 1:
        data_agent = data_agent[:, 0]

    min_len = min(len(data_ref), len(data_agent))
    max_len = max(len(data_ref), len(data_agent))

    duration_penalty = (max_len - min_len) / rate_ref

    if min_len == 0:
        mse = 999999.0
    else:
        diff = data_ref[:min_len].astype(np.float32) - data_agent[:min_len].astype(np.float32)
        mse = np.mean(diff ** 2)

    total_error = mse + (duration_penalty * 10000)

    threshold = 100.0
    assert total_error <= threshold, f"Total error metric {total_error} exceeds threshold {threshold}. MSE: {mse}, Duration Penalty: {duration_penalty}"