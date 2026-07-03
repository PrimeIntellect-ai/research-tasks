# test_final_state.py
import os
import subprocess
import pytest
from pathlib import Path

def test_compilation():
    project_dir = "/home/user/project"
    cpp_file = os.path.join(project_dir, "sanitise_deps.cpp")
    makefile = os.path.join(project_dir, "Makefile")
    executable = os.path.join(project_dir, "sanitise_deps")

    assert os.path.isfile(cpp_file), f"Source file {cpp_file} is missing."
    assert os.path.isfile(makefile), f"Makefile {makefile} is missing."

    # Run make to compile the project
    result = subprocess.run(["make"], cwd=project_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Compilation failed. Make output:\n{result.stdout}\n{result.stderr}"

    assert os.path.isfile(executable), "Executable 'sanitise_deps' was not created by make."
    assert os.access(executable, os.X_OK), "Executable 'sanitise_deps' does not have execute permissions."

def test_adversarial_corpus():
    project_dir = "/home/user/project"
    executable = os.path.join(project_dir, "sanitise_deps")

    assert os.path.isfile(executable), "Executable missing. Compilation must have failed."

    evil_dir = Path("/app/tests/evil")
    clean_dir = Path("/app/tests/clean")

    evil_files = [f for f in evil_dir.iterdir() if f.is_file()]
    clean_files = [f for f in clean_dir.iterdir() if f.is_file()]

    assert len(evil_files) > 0, "Evil corpus is empty or missing."
    assert len(clean_files) > 0, "Clean corpus is empty or missing."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (should be REJECTED)
    for f in evil_files:
        result = subprocess.run([executable, str(f)], cwd=project_dir, capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            evil_bypassed.append(f.name)

    # Test clean corpus (should be ACCEPTED)
    for f in clean_files:
        result = subprocess.run([executable, str(f)], cwd=project_dir, capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            clean_modified.append(f.name)

    # Surface a clear summary on failure
    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))