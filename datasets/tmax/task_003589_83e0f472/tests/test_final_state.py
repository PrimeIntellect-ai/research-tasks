# test_final_state.py
import os
import wave
import struct
import math
import pytest

def test_output_wav_exists():
    assert os.path.isfile('/app/output.wav'), "The output file '/app/output.wav' was not generated."

def test_output_wav_rms_convergence():
    wav_path = '/app/output.wav'
    assert os.path.isfile(wav_path), f"Cannot calculate RMS because {wav_path} does not exist."

    with wave.open(wav_path, 'rb') as w:
        n_frames = w.getnframes()
        assert n_frames > 0, "The output.wav file is empty."

        frames = w.readframes(n_frames)
        samples = struct.unpack(f'<{n_frames}h', frames)

        sq_sum = sum(s * s for s in samples)
        rms = math.sqrt(sq_sum / len(samples))

    threshold = 15000
    assert rms < threshold, (
        f"The filter failed to converge properly. "
        f"Expected RMS < {threshold}, but got {rms:.2f}. "
        f"This indicates the NLMS update rule was not implemented correctly."
    )