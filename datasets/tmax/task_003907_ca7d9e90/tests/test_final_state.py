# test_final_state.py
import os
import shutil
import tempfile
import subprocess
import pytest

def test_cleanup_script_behavior():
    script_path = "/home/user/cleanup.py"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    clean_corpus_path = "/app/corpora/clean"
    evil_corpus_path = "/app/corpora/evil"

    assert os.path.isdir(clean_corpus_path), "Clean corpus missing."
    assert os.path.isdir(evil_corpus_path), "Evil corpus missing."

    clean_files = os.listdir(clean_corpus_path)
    evil_files = os.listdir(evil_corpus_path)

    with tempfile.TemporaryDirectory() as staging_dir:
        # Copy all files to staging directory
        for f in clean_files:
            shutil.copy(os.path.join(clean_corpus_path, f), staging_dir)
        for f in evil_files:
            shutil.copy(os.path.join(evil_corpus_path, f), staging_dir)

        # Run the agent's script
        result = subprocess.run(
            ["python3", script_path, staging_dir],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

        # Check the resulting files in the staging directory
        staging_files = os.listdir(staging_dir)

        evil_bypassed = []
        for f in evil_files:
            if f in staging_files or f"approved_{f}" in staging_files:
                evil_bypassed.append(f)

        clean_modified_or_missing = []
        for f in clean_files:
            expected_name = f"approved_{f}"
            if expected_name not in staging_files:
                clean_modified_or_missing.append(f)

        # Check for extracted files/directories
        extracted_items = []
        for item in staging_files:
            item_path = os.path.join(staging_dir, item)
            if os.path.isdir(item_path):
                extracted_items.append(item)
            elif item not in evil_files and not item.startswith("approved_"):
                # If it's not an evil file that was bypassed, and not an approved file, it might be an extracted file
                extracted_items.append(item)

        error_messages = []
        if evil_bypassed:
            error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified_or_missing:
            error_messages.append(f"{len(clean_modified_or_missing)} of {len(clean_files)} clean modified or missing: {', '.join(clean_modified_or_missing)}")
        if extracted_items:
            error_messages.append(f"Archives were extracted to disk or unexpected files created: {', '.join(extracted_items)}")

        if error_messages:
            pytest.fail(" | ".join(error_messages))