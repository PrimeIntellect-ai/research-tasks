# test_final_state.py

import os
import subprocess
import tempfile
import filecmp
import pytest

def test_log_pipeline_builds():
    """
    Verify that the Rust project in /home/user/log_pipeline builds successfully.
    """
    pipeline_dir = "/home/user/log_pipeline"
    assert os.path.isdir(pipeline_dir), f"Directory {pipeline_dir} is missing"

    result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=pipeline_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"log_pipeline failed to build:\n{result.stderr}"

def test_sanitiser_against_corpora():
    """
    Verify the sanitiser correctly processes the clean and evil corpora.
    """
    sanitiser_dir = "/home/user/sanitiser"
    assert os.path.isdir(sanitiser_dir), f"Sanitiser directory {sanitiser_dir} is missing"

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    # Check if the sanitiser builds
    build_result = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=sanitiser_dir,
        capture_output=True,
        text=True
    )
    assert build_result.returncode == 0, f"sanitiser failed to build:\n{build_result.stderr}"

    sanitiser_bin = os.path.join(sanitiser_dir, "target", "release", "sanitiser")
    if not os.path.isfile(sanitiser_bin):
        # Fallback to cargo run if binary name is different
        run_cmd = ["cargo", "run", "--release", "--"]
    else:
        run_cmd = [sanitiser_bin]

    with tempfile.TemporaryDirectory() as evil_out, tempfile.TemporaryDirectory() as clean_out:
        # Run on evil corpus
        evil_result = subprocess.run(
            run_cmd + [evil_dir, evil_out],
            cwd=sanitiser_dir,
            capture_output=True,
            text=True
        )
        assert evil_result.returncode == 0, f"Sanitiser failed on evil corpus:\n{evil_result.stderr}"

        # Run on clean corpus
        clean_result = subprocess.run(
            run_cmd + [clean_dir, clean_out],
            cwd=sanitiser_dir,
            capture_output=True,
            text=True
        )
        assert clean_result.returncode == 0, f"Sanitiser failed on clean corpus:\n{clean_result.stderr}"

        # Verify clean corpus: 100% preserved unchanged
        clean_files = os.listdir(clean_dir)
        clean_modified = []
        for f in clean_files:
            in_path = os.path.join(clean_dir, f)
            out_path = os.path.join(clean_out, f)
            if not os.path.isfile(out_path):
                clean_modified.append(f"{f} (missing)")
            elif not filecmp.cmp(in_path, out_path, shallow=False):
                clean_modified.append(f"{f} (modified)")

        # Verify evil corpus: 100% rejected (assuming files are entirely evil, output should be empty or missing)
        evil_files = os.listdir(evil_dir)
        evil_bypassed = []
        for f in evil_files:
            out_path = os.path.join(evil_out, f)
            if os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
                evil_bypassed.append(f)

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))