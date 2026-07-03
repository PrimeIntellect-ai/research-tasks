# test_final_state.py

import os
import shutil
import subprocess
import tempfile
import glob
import pytest

def test_filter_script_behavior():
    script_path = "/home/user/filter.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_corpus, "*.fasta"))
    evil_files = glob.glob(os.path.join(evil_corpus, "*.fasta"))

    assert len(clean_files) > 0, "No clean files found in corpus"
    assert len(evil_files) > 0, "No evil files found in corpus"

    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        # Copy all files to input_dir
        for f in clean_files:
            shutil.copy(f, input_dir)
        for f in evil_files:
            shutil.copy(f, input_dir)

        # Run the script
        result = subprocess.run(
            [script_path, input_dir, output_dir],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Script failed with exit code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        # Check output directory
        output_files = set(os.listdir(output_dir))
        clean_basenames = {os.path.basename(f) for f in clean_files}
        evil_basenames = {os.path.basename(f) for f in evil_files}

        missing_clean = clean_basenames - output_files
        bypassed_evil = output_files.intersection(evil_basenames)

        error_msgs = []
        if bypassed_evil:
            error_msgs.append(f"{len(bypassed_evil)} of {len(evil_basenames)} evil bypassed: {', '.join(list(bypassed_evil)[:5])}")
        if missing_clean:
            error_msgs.append(f"{len(missing_clean)} of {len(clean_basenames)} clean modified/missing: {', '.join(list(missing_clean)[:5])}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))