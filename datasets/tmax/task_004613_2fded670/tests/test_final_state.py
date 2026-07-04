# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_networkx_installed():
    """Verify that networkx is properly installed and importable."""
    try:
        import networkx as nx
        assert hasattr(nx, 'node_link_graph'), "networkx is installed but missing node_link_graph; installation may be corrupted."
    except ImportError:
        pytest.fail("networkx is not installed or importable. The setup.py fix or installation failed.")

def test_script_exists():
    """Verify the student created the detection script at the correct path."""
    script_path = "/home/user/detect_violations.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_detector_evil_corpus():
    """Verify the script correctly flags all files in the evil corpus."""
    evil_dir = "/app/corpus/evil"
    script_path = "/home/user/detect_violations.py"

    with tempfile.NamedTemporaryFile(mode='r+', delete=False) as tmp_out:
        out_file = tmp_out.name

    try:
        result = subprocess.run(
            ["python3", script_path, evil_dir, out_file],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed execution on evil corpus. STDERR:\n{result.stderr}"

        with open(out_file, 'r') as f:
            flagged = set(line.strip() for line in f if line.strip())

        evil_files = set(f for f in os.listdir(evil_dir) if f.endswith('.json'))
        missed = evil_files - flagged

        assert not missed, f"{len(missed)} of {len(evil_files)} evil bypassed detection. Missed files: {', '.join(missed)}"
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)

def test_detector_clean_corpus():
    """Verify the script correctly ignores all files in the clean corpus."""
    clean_dir = "/app/corpus/clean"
    script_path = "/home/user/detect_violations.py"

    with tempfile.NamedTemporaryFile(mode='r+', delete=False) as tmp_out:
        out_file = tmp_out.name

    try:
        result = subprocess.run(
            ["python3", script_path, clean_dir, out_file],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed execution on clean corpus. STDERR:\n{result.stderr}"

        with open(out_file, 'r') as f:
            flagged = set(line.strip() for line in f if line.strip())

        clean_files = set(f for f in os.listdir(clean_dir) if f.endswith('.json'))
        false_positives = clean_files & flagged

        assert not false_positives, f"{len(false_positives)} of {len(clean_files)} clean modified/flagged incorrectly. Offending files: {', '.join(false_positives)}"
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)