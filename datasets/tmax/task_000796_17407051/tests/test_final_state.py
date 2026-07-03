# test_final_state.py

import os
import subprocess
import tempfile
import numpy as np
from scipy.io import wavfile
import pytest

SCRIPT_PATH = "/home/user/wave_math.py"
REF_AUDIO_PATH = "/app/reference_audio.wav"
PROCESSED_AUDIO_PATH = "/home/user/processed_audio.wav"
EVIL_CORPUS_PATH = "/tests/corpora/evil_expressions.txt"
CLEAN_CORPUS_PATH = "/tests/corpora/clean_expressions.txt"

def test_processed_audio_correctness():
    assert os.path.isfile(PROCESSED_AUDIO_PATH), f"Processed audio file {PROCESSED_AUDIO_PATH} not found."

    # Compute expected output
    rate, data = wavfile.read(REF_AUDIO_PATH)
    expected_data = data * 2.0

    # Read actual output
    act_rate, act_data = wavfile.read(PROCESSED_AUDIO_PATH)

    assert act_rate == rate, f"Sample rate mismatch: expected {rate}, got {act_rate}"
    np.testing.assert_allclose(act_data, expected_data, err_msg="Processed audio data does not match the expected output of x * 2.0")

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} not found."
    assert os.path.isfile(EVIL_CORPUS_PATH), f"Evil corpus {EVIL_CORPUS_PATH} not found."
    assert os.path.isfile(CLEAN_CORPUS_PATH), f"Clean corpus {CLEAN_CORPUS_PATH} not found."

    with open(EVIL_CORPUS_PATH, "r") as f:
        evil_exprs = [line.strip() for line in f if line.strip()]

    with open(CLEAN_CORPUS_PATH, "r") as f:
        clean_exprs = [line.strip() for line in f if line.strip()]

    evil_bypassed = []
    clean_failed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        out_wav = os.path.join(tmpdir, "out.wav")

        # Test evil corpus
        for expr in evil_exprs:
            res = subprocess.run(
                ["python3", SCRIPT_PATH, REF_AUDIO_PATH, out_wav, expr],
                capture_output=True
            )
            # Should exit with non-zero status (1 expected)
            if res.returncode == 0:
                evil_bypassed.append(expr)

        # Test clean corpus
        for expr in clean_exprs:
            if os.path.exists(out_wav):
                os.remove(out_wav)
            res = subprocess.run(
                ["python3", SCRIPT_PATH, REF_AUDIO_PATH, out_wav, expr],
                capture_output=True
            )
            # Should exit with 0 and create the output file
            if res.returncode != 0 or not os.path.isfile(out_wav):
                clean_failed.append(expr)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_exprs)} evil bypassed: {evil_bypassed}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_exprs)} clean modified/failed: {clean_failed}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))