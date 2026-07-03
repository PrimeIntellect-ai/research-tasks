# test_final_state.py

import os
import sys
import csv
import subprocess
import pytest
import numpy as np

def test_tiny_embedder_fixed():
    """Verify that the bug is fixed in tiny-embedder core.py."""
    core_py = "/app/tiny-embedder/tiny_embedder/core.py"
    assert os.path.isfile(core_py), f"File missing: {core_py}"
    with open(core_py, "r") as f:
        content = f.read()

    assert "axis=1" in content, "The bug (axis=0) was not fixed to axis=1 in core.py"
    assert "axis=0" not in content, "The bug (axis=0) is still present in core.py"

def test_tiny_embedder_installed():
    """Verify that the tiny-embedder package is installed and works correctly."""
    try:
        import tiny_embedder
    except ImportError:
        pytest.fail("tiny_embedder is not installed in the environment.")

    embedder = tiny_embedder.TinyEmbedder()
    vecs = embedder.embed(["hello world", "test"])
    norms = np.linalg.norm(vecs, axis=1)
    np.testing.assert_allclose(norms, [1.0, 1.0], err_msg="Embeddings are not L2-normalized correctly. The fix might be incorrect.")

def test_script_exists():
    """Verify that the filter_csv.py script exists."""
    script_path = "/home/user/filter_csv.py"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"

def test_adversarial_corpus_filtering(tmp_path):
    """Run the agent's script on clean and evil corpora and verify the output."""
    script_path = "/home/user/filter_csv.py"
    clean_dir = "/home/user/data/clean"
    evil_dir = "/home/user/data/evil"

    # Test Clean Corpus
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".csv")]
    clean_modified = []

    for cf in clean_files:
        input_csv = os.path.join(clean_dir, cf)
        output_csv = os.path.join(tmp_path, f"out_{cf}")

        # Read original rows
        with open(input_csv, "r") as f:
            original_rows = list(csv.DictReader(f))

        # Run script
        res = subprocess.run([sys.executable, script_path, "--input", input_csv, "--output", str(output_csv)], capture_output=True, text=True)
        assert res.returncode == 0, f"Script failed on clean file {cf}:\n{res.stderr}"

        # Read output rows
        with open(output_csv, "r") as f:
            output_rows = list(csv.DictReader(f))

        if len(output_rows) != len(original_rows):
            clean_modified.append(cf)

    # Test Evil Corpus
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".csv")]
    evil_bypassed = []

    for ef in evil_files:
        input_csv = os.path.join(evil_dir, ef)
        output_csv = os.path.join(tmp_path, f"out_{ef}")

        # Run script
        res = subprocess.run([sys.executable, script_path, "--input", input_csv, "--output", str(output_csv)], capture_output=True, text=True)
        assert res.returncode == 0, f"Script failed on evil file {ef}:\n{res.stderr}"

        # Read output rows
        with open(output_csv, "r") as f:
            output_rows = list(csv.DictReader(f))

        if len(output_rows) > 0:
            evil_bypassed.append(ef)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail("; ".join(error_msgs))