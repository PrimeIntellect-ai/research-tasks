# test_final_state.py

import os
import subprocess
from pathlib import Path
import pytest

def get_sanitizer_cmd():
    sh_path = Path("/home/user/sanitizer.sh")
    py_path = Path("/home/user/sanitizer.py")

    if sh_path.exists():
        if os.access(sh_path, os.X_OK):
            return [str(sh_path)]
        else:
            return ["bash", str(sh_path)]
    elif py_path.exists():
        if os.access(py_path, os.X_OK):
            return [str(py_path)]
        else:
            return ["python3", str(py_path)]
    return None

def run_sanitizer(cmd, input_data: bytes) -> bytes:
    result = subprocess.run(
        cmd,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10
    )
    return result.stdout

def test_sanitizer_exists():
    cmd = get_sanitizer_cmd()
    assert cmd is not None, "Sanitizer script not found at /home/user/sanitizer.sh or /home/user/sanitizer.py"

def test_clean_corpus():
    cmd = get_sanitizer_cmd()
    assert cmd is not None, "Sanitizer script not found."

    clean_dir = Path("/app/corpora/clean")
    assert clean_dir.exists() and clean_dir.is_dir(), "Clean corpus directory missing."

    failed_files = []
    total_files = 0

    for csv_file in clean_dir.glob("*.csv"):
        total_files += 1
        input_data = csv_file.read_bytes()
        output_data = run_sanitizer(cmd, input_data)

        # Parse lines to ignore trailing newlines
        input_lines = [line for line in input_data.decode('utf-8', errors='replace').splitlines() if line.strip()]
        output_lines = [line for line in output_data.decode('utf-8', errors='replace').splitlines() if line.strip()]

        if input_lines != output_lines:
            failed_files.append(csv_file.name)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total_files} clean files modified: {', '.join(failed_files)}")

def test_evil_corpus():
    cmd = get_sanitizer_cmd()
    assert cmd is not None, "Sanitizer script not found."

    evil_dir = Path("/app/corpora/evil")
    assert evil_dir.exists() and evil_dir.is_dir(), "Evil corpus directory missing."

    failed_files = []
    total_files = 0

    for csv_file in evil_dir.glob("*.csv"):
        total_files += 1
        input_data = csv_file.read_bytes()
        output_data = run_sanitizer(cmd, input_data)

        output_lines = [line for line in output_data.decode('utf-8', errors='replace').splitlines() if line.strip()]

        if len(output_lines) > 0:
            failed_files.append(csv_file.name)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total_files} evil files bypassed: {', '.join(failed_files)}")