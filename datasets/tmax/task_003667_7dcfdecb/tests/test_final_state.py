# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_detector_exists_and_executable():
    """Verify that the compiled detector exists and is executable."""
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}"
    st = os.stat(detector_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Detector at {detector_path} is not executable"

def test_detector_uses_openmp():
    """Verify that the compiled detector is linked against libgomp."""
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}"

    result = subprocess.run(["ldd", detector_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run ldd on detector"
    assert "libgomp" in result.stdout, "Detector is not dynamically linked to libgomp (OpenMP not properly enabled)"

def test_makefile_fixed():
    """Verify that the Makefile in the vendored library was fixed."""
    makefile_path = "/app/vendored/seq-mcmc-1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-fomp" not in content, "The deliberate typo '-fomp' is still present in the Makefile"
    assert "-fopenmp" in content, "The correct '-fopenmp' flag was not found in the Makefile"

def test_adversarial_corpus():
    """Test the detector against the clean and evil corpora."""
    detector_path = "/home/user/detector"
    assert os.path.isfile(detector_path), f"Detector executable not found at {detector_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed_clean = []
    failed_evil = []

    for cf in clean_files:
        result = subprocess.run([detector_path, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([detector_path, ef], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean files modified/rejected (expected exit code 0): {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (expected exit code 1): {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)