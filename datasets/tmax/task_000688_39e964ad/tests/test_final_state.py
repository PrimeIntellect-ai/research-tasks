# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import pytest

def test_text_sampler_installed():
    """Verify that the text-sampler package is installed and accessible."""
    try:
        result = subprocess.run(
            ["text-sampler", "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert result.returncode == 0, "text-sampler command failed to run. Is it installed correctly?"
    except FileNotFoundError:
        pytest.fail("text-sampler command not found. The package was not installed or not in PATH.")

def test_filter_data_script():
    """Verify filter_data.sh against the hidden adversarial corpus."""
    script_path = "/home/user/filter_data.sh"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    clean_dir = "/verify/corpora/clean/"
    evil_dir = "/verify/corpora/evil/"

    assert os.path.isdir(clean_dir), f"Hidden clean corpus missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Hidden evil corpus missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([script_path, cf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        res = subprocess.run([script_path, ef], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_pipeline_script():
    """Verify pipeline.sh correctly processes a directory using filter_data.sh and text-sampler."""
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"Pipeline script not found: {pipeline_path}"
    assert os.access(pipeline_path, os.X_OK), f"Pipeline script is not executable: {pipeline_path}"

    with tempfile.TemporaryDirectory() as tmp_in, tempfile.TemporaryDirectory() as tmp_out:
        # Create a clean file
        clean_file = os.path.join(tmp_in, "clean.txt")
        with open(clean_file, "w") as f:
            f.write("SCHEMA_VERSION=1.0\n")
            for i in range(10):
                f.write(f"Line {i}\n")

        # Create an evil file (missing schema)
        evil_file = os.path.join(tmp_in, "evil.txt")
        with open(evil_file, "w") as f:
            f.write("WRONG_SCHEMA=1.0\n")
            for i in range(10):
                f.write(f"Line {i}\n")

        # Run pipeline
        res = subprocess.run([pipeline_path, tmp_in, tmp_out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert res.returncode == 0, f"pipeline.sh failed with exit code {res.returncode}"

        # Check outputs
        out_files = os.listdir(tmp_out)

        assert "clean.txt.sample" in out_files, "Pipeline failed to produce .sample for clean file"
        assert "evil.txt.sample" not in out_files, "Pipeline produced .sample for evil file"

        clean_sample_path = os.path.join(tmp_out, "clean.txt.sample")
        with open(clean_sample_path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 5, f"Expected exactly 5 lines in sample, got {len(lines)}"