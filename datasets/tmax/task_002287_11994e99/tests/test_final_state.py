# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_detector_executable_exists():
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"The detector executable {detector_path} does not exist. Did you compile it?"
    assert os.access(detector_path, os.X_OK), f"The detector executable {detector_path} is not executable."

def test_adversarial_corpus():
    detector_path = "/home/user/detector"

    evil_dir = "/app/hidden_corpus/evil"
    clean_dir = "/app/hidden_corpus/clean"

    evil_wavs = sorted(glob.glob(os.path.join(evil_dir, "*.wav")))
    clean_wavs = sorted(glob.glob(os.path.join(clean_dir, "*.wav")))

    assert len(evil_wavs) > 0, f"No evil wav files found in {evil_dir}."
    assert len(clean_wavs) > 0, f"No clean wav files found in {clean_dir}."

    bypassed_evil = []
    for wav in evil_wavs:
        res = subprocess.run([detector_path, wav], capture_output=True)
        # Expected exit code 1 for EVIL
        if res.returncode != 1:
            bypassed_evil.append(os.path.basename(wav))

    modified_clean = []
    for wav in clean_wavs:
        res = subprocess.run([detector_path, wav], capture_output=True)
        # Expected exit code 0 for CLEAN
        if res.returncode != 0:
            modified_clean.append(os.path.basename(wav))

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_wavs)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_wavs)} clean modified: {', '.join(modified_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))