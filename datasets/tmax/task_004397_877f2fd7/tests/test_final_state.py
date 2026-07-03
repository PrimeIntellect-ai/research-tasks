# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_compiles_and_works():
    c_source = "/home/user/detector.c"
    executable = "/home/user/detector"

    assert os.path.isfile(c_source), f"Source file {c_source} does not exist."

    # Compile the detector
    compile_cmd = ["gcc", c_source, "-o", executable]
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile {c_source}:\n{compile_proc.stderr}"
    assert os.path.isfile(executable), f"Executable {executable} was not created."
    assert os.access(executable, os.X_OK), f"Executable {executable} is not executable."

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for f in evil_files:
        proc = subprocess.run([executable, f], capture_output=True)
        if proc.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        proc = subprocess.run([executable, f], capture_output=True)
        if proc.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)