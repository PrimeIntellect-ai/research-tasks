# test_final_state.py

import os
import subprocess
import pytest

def test_compile_sanitizer():
    source_file = "/home/user/sanitizer.c"
    executable = "/home/user/sanitizer"

    assert os.path.exists(source_file), f"Source file {source_file} not found. The student must create the sanitizer source code."

    compile_cmd = ["gcc", "-O2", source_file, "-o", executable]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Compilation failed. Standard error output:\n{result.stderr}"
    assert os.path.exists(executable), f"Executable {executable} not found after compilation."

def test_adversarial_corpus():
    executable = "/home/user/sanitizer"
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.exists(executable), f"Sanitizer executable {executable} not found. Ensure compilation succeeds."
    assert os.path.exists(evil_dir), f"Evil corpus directory {evil_dir} not found."
    assert os.path.exists(clean_dir), f"Clean corpus directory {clean_dir} not found."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for f in evil_files:
        file_path = os.path.join(evil_dir, f)
        result = subprocess.run([executable, file_path], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "EVIL":
            evil_bypassed.append(f)

    # Test clean corpus
    for f in clean_files:
        file_path = os.path.join(clean_dir, f)
        result = subprocess.run([executable, file_path], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)