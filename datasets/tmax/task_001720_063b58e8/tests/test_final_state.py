# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_filter_script_exists():
    assert os.path.isfile('/home/user/filter.sh'), "/home/user/filter.sh does not exist."

def test_adversarial_corpus():
    script_path = '/home/user/filter.sh'
    assert os.path.isfile(script_path), "Script /home/user/filter.sh is missing."

    evil_dir = '/app/corpus/evil'
    clean_dir = '/app/corpus/clean'

    evil_files = glob.glob(os.path.join(evil_dir, '*.wav'))
    clean_files = glob.glob(os.path.join(clean_dir, '*.wav'))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"

    evil_bypassed = []
    clean_rejected = []

    # Test Evil Corpus (Expect exit code 1)
    for evil_file in evil_files:
        result = subprocess.run(['bash', script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test Clean Corpus (Expect exit code 0)
    for clean_file in clean_files:
        result = subprocess.run(['bash', script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))