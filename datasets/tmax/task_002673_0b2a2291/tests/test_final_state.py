# test_final_state.py

import os
import subprocess
import shutil
import struct
import pytest

EXECUTABLE = "/home/user/secure_extractor"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def parse_archive(archive_path):
    """Parses the custom archive format and yields (filename, data)."""
    with open(archive_path, 'rb') as f:
        while True:
            l_bytes = f.read(2)
            if not l_bytes:
                break
            if len(l_bytes) < 2:
                break
            name_len = struct.unpack('<H', l_bytes)[0]
            filename = f.read(name_len).decode('ascii')
            s_bytes = f.read(4)
            if len(s_bytes) < 4:
                break
            data_len = struct.unpack('<I', s_bytes)[0]
            data = f.read(data_len)
            yield filename, data

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} not found. Did you compile the code?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus dir {CLEAN_CORPUS_DIR} missing")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_clean = []

    for filename in clean_files:
        archive_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        target_dir = f"/tmp/clean_extraction_{filename}"

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)

        with open(archive_path, 'rb') as stdin_f:
            result = subprocess.run(
                [EXECUTABLE, target_dir],
                stdin=stdin_f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        stdout_out = result.stdout.strip()

        if result.returncode != 0 or stdout_out != "CLEAN":
            failed_clean.append(f"{filename} (exit {result.returncode}, stdout: {stdout_out})")
            continue

        # Verify extracted files
        expected_entries = list(parse_archive(archive_path))
        for exp_name, exp_data in expected_entries:
            # Handle possible subdirectories in clean archives
            exp_path = os.path.join(target_dir, exp_name)
            if not os.path.isfile(exp_path):
                failed_clean.append(f"{filename} missing extracted file {exp_name}")
                break
            with open(exp_path, 'rb') as f:
                actual_data = f.read()
            if actual_data != exp_data:
                failed_clean.append(f"{filename} extracted data mismatch for {exp_name}")
                break

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean archives failed to extract properly:\n" + "\n".join(failed_clean))

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus dir {EVIL_CORPUS_DIR} missing")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_evil = []

    for filename in evil_files:
        archive_path = os.path.join(EVIL_CORPUS_DIR, filename)
        target_dir = f"/tmp/evil_extraction_{filename}"

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)

        with open(archive_path, 'rb') as stdin_f:
            result = subprocess.run(
                [EXECUTABLE, target_dir],
                stdin=stdin_f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        stdout_out = result.stdout.strip()

        if result.returncode != 1 or stdout_out != "MALICIOUS":
            failed_evil.append(f"{filename} bypassed (exit {result.returncode}, stdout: {stdout_out})")
            continue

        # Verify rollback (target dir must be completely empty)
        extracted_files = os.listdir(target_dir)
        if len(extracted_files) > 0:
            failed_evil.append(f"{filename} left files in target dir: {extracted_files}")
            continue

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(evil_files)} evil archives bypassed checks:\n" + "\n".join(failed_evil))