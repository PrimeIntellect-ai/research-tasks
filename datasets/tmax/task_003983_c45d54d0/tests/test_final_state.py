# test_final_state.py

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import pytest

def test_fast_filter_exists_and_executable():
    filter_path = Path("/home/user/fast_filter")
    assert filter_path.exists(), "The fast_filter binary does not exist at /home/user/fast_filter."
    assert filter_path.is_file(), "/home/user/fast_filter is not a file."
    assert os.access(filter_path, os.X_OK), "The fast_filter binary is not executable."

def test_fast_filter_correctness():
    filter_path = Path("/home/user/fast_filter")
    evil_corpus_dir = Path("/var/opt/eval_data/evil")
    clean_corpus_dir = Path("/var/opt/eval_data/clean")

    assert evil_corpus_dir.exists() and evil_corpus_dir.is_dir(), "Evil corpus directory missing."
    assert clean_corpus_dir.exists() and clean_corpus_dir.is_dir(), "Clean corpus directory missing."

    evil_files = list(evil_corpus_dir.glob("*.bin"))
    clean_files = list(clean_corpus_dir.glob("*.bin"))

    assert len(evil_files) > 0, "No evil files found in corpus."
    assert len(clean_files) > 0, "No clean files found in corpus."

    with tempfile.TemporaryDirectory() as temp_input, tempfile.TemporaryDirectory() as temp_output:
        temp_input_path = Path(temp_input)
        temp_output_path = Path(temp_output)

        # Create expected output directories
        (temp_output_path / "clean").mkdir(parents=True, exist_ok=True)
        (temp_output_path / "evil").mkdir(parents=True, exist_ok=True)

        # Copy all corpus files to the flat input directory
        for f in evil_files:
            shutil.copy(f, temp_input_path / f.name)
        for f in clean_files:
            shutil.copy(f, temp_input_path / f.name)

        # Run the agent's filter
        result = subprocess.run(
            [str(filter_path), str(temp_input_path), str(temp_output_path)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"fast_filter exited with non-zero code {result.returncode}. stderr: {result.stderr}"

        # Check evil files
        evil_bypassed = []
        for f in evil_files:
            expected_path = temp_output_path / "evil" / f.name
            if not expected_path.exists():
                evil_bypassed.append(f.name)

        # Check clean files
        clean_modified = []
        for f in clean_files:
            expected_path = temp_output_path / "clean" / f.name
            if not expected_path.exists():
                clean_modified.append(f.name)

        error_messages = []
        if evil_bypassed:
            error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:10])}{'...' if len(evil_bypassed) > 10 else ''}")
        if clean_modified:
            error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (misclassified as evil or missing): {', '.join(clean_modified[:10])}{'...' if len(clean_modified) > 10 else ''}")

        assert not error_messages, " | ".join(error_messages)