# test_final_state.py
import os
import sys
import subprocess
import pytest

def test_fast_covar_installed():
    """Verify that the fast_covar package was successfully fixed and installed."""
    try:
        import fast_covar
    except ImportError:
        pytest.fail("fast_covar is not installed or importable. The agent failed to fix and install the vendored package.")

def test_detector_exists():
    """Verify that the detector script exists at the correct path."""
    assert os.path.exists("/home/user/detector.py"), "/home/user/detector.py does not exist."

def test_detector_clean_corpus():
    """Verify that the detector accepts all clean datasets (exit code 0)."""
    clean_dir = "/home/user/data/clean"
    assert os.path.exists(clean_dir), f"Clean data directory missing: {clean_dir}"

    modified_clean = []
    total_clean = 0

    for d in sorted(os.listdir(clean_dir)):
        ds_path = os.path.join(clean_dir, d)
        if os.path.isdir(ds_path):
            total_clean += 1
            result = subprocess.run([sys.executable, "/home/user/detector.py", ds_path])
            if result.returncode != 0:
                modified_clean.append(d)

    assert len(modified_clean) == 0, f"{len(modified_clean)} of {total_clean} clean modified/rejected: {modified_clean}"

def test_detector_evil_corpus():
    """Verify that the detector rejects all evil datasets (exit code 1)."""
    evil_dir = "/home/user/data/evil"
    assert os.path.exists(evil_dir), f"Evil data directory missing: {evil_dir}"

    bypassed_evil = []
    total_evil = 0

    for d in sorted(os.listdir(evil_dir)):
        ds_path = os.path.join(evil_dir, d)
        if os.path.isdir(ds_path):
            total_evil += 1
            result = subprocess.run([sys.executable, "/home/user/detector.py", ds_path])
            if result.returncode != 1:
                bypassed_evil.append(d)

    assert len(bypassed_evil) == 0, f"{len(bypassed_evil)} of {total_evil} evil bypassed: {bypassed_evil}"