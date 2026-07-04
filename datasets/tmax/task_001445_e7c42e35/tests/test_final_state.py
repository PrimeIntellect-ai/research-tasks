# test_final_state.py

import os
import subprocess
import pytest

def test_stage1_makefile_fixed_and_compiled():
    """Verify that the Makefile was fixed and libjit.so builds as a shared library."""
    makefile_path = "/home/user/libjit/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."

    with open(makefile_path, "r") as f:
        makefile_content = f.read()

    assert "-fPIC" in makefile_content, "Makefile does not include -fPIC flag."
    assert "-shared" in makefile_content, "Makefile does not include -shared flag."

    # Try to build
    build_result = subprocess.run(["make", "-C", "/home/user/libjit"], capture_output=True, text=True)
    assert build_result.returncode == 0, f"make failed: {build_result.stderr}"

    so_path = "/home/user/libjit/libjit.so"
    assert os.path.isfile(so_path), "libjit.so was not generated."

    # Verify it is a shared object
    file_cmd = subprocess.run(["file", so_path], capture_output=True, text=True)
    assert "shared object" in file_cmd.stdout, f"libjit.so is not a shared object: {file_cmd.stdout}"

def test_stage2_red_frames_extracted():
    """Verify that the correct red frames were extracted from the video."""
    output_path = "/home/user/red_frames.txt"
    assert os.path.isfile(output_path), "red_frames.txt is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["12", "25", "48"]
    assert lines == expected, f"Expected red frames {expected}, but got {lines}."

def test_stage3_sanitizer_adversarial_corpus():
    """Verify that the sanitizer correctly rejects evil payloads and accepts clean ones."""
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), "sanitizer.py is missing."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".json")]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".json")]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        full_path = os.path.join(evil_dir, evil_file)
        result = subprocess.run(["python3", sanitizer_path, full_path], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "EVIL":
            evil_bypassed.append(evil_file)

    # Test clean corpus
    for clean_file in clean_files:
        full_path = os.path.join(clean_dir, clean_file)
        result = subprocess.run(["python3", sanitizer_path, full_path], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_modified.append(clean_file)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msg)