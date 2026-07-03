# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/process_configs.sh"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def get_device_type(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()

    # Skip 16 byte header
    text_content = content[16:].decode('utf-8', errors='ignore')
    for line in text_content.splitlines():
        if line.startswith("DeviceType: "):
            return line.split("DeviceType: ")[1].strip()
    return None

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_clean_corpus_processed_correctly():
    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run(["bash", SCRIPT_PATH, CLEAN_CORPUS, out_dir], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on clean corpus. stderr: {result.stderr}"

        clean_files = os.listdir(CLEAN_CORPUS)
        missing = []
        wrong_group = []

        for fname in clean_files:
            src_path = os.path.join(CLEAN_CORPUS, fname)
            device_type = get_device_type(src_path)
            if not device_type:
                continue 

            expected_out_path = os.path.join(out_dir, device_type, fname)
            if not os.path.exists(expected_out_path):
                found = False
                for root, dirs, files in os.walk(out_dir):
                    if fname in files:
                        wrong_group.append(fname)
                        found = True
                        break
                if not found:
                    missing.append(fname)

        assert not missing, f"{len(missing)} of {len(clean_files)} clean files missing from output. Offending files: {missing[:5]}"
        assert not wrong_group, f"{len(wrong_group)} of {len(clean_files)} clean files placed in wrong subdirectory. Offending files: {wrong_group[:5]}"

def test_evil_corpus_rejected():
    with tempfile.TemporaryDirectory() as out_dir:
        subprocess.run(["bash", SCRIPT_PATH, EVIL_CORPUS, out_dir], capture_output=True, text=True)

        evil_files = os.listdir(EVIL_CORPUS)
        bypassed = []

        for root, dirs, files in os.walk(out_dir):
            for fname in files:
                bypassed.append(fname)

        assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil configurations bypassed validation. Offending files: {bypassed[:5]}"