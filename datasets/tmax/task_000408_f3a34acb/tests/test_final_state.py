# test_final_state.py
import os
import stat
import subprocess
import pytest
import tarfile

def test_archive_tool_fixed():
    script_path = "/app/bash-archive-tool-1.0.0/archive.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"Script {script_path} is not executable."

    output_archive = "/tmp/test_archive.tar.gz"
    input_dir = "/app/corpus/clean/"

    if os.path.exists(output_archive):
        os.remove(output_archive)

    result = subprocess.run([script_path, output_archive, input_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Archive script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(output_archive), f"Archive script did not create the output archive at {output_archive}."

    # Verify it is a valid tar.gz
    try:
        with tarfile.open(output_archive, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) > 0, "Archive is empty."
    except tarfile.ReadError:
        pytest.fail(f"Archive {output_archive} is not a valid gzip-compressed tar archive.")

def test_classifier_adversarial_corpus():
    classifier_path = "/home/user/classifier.sh"
    assert os.path.isfile(classifier_path), f"Classifier script missing at {classifier_path}"

    st = os.stat(classifier_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"Classifier {classifier_path} is not executable."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    bypassed_evil = []
    modified_clean = []

    for f in evil_files:
        result = subprocess.run([classifier_path, f], capture_output=True, text=True)
        out = result.stdout.strip()
        if result.returncode != 1 or out != "EVIL":
            bypassed_evil.append(os.path.basename(f))

    for f in clean_files:
        result = subprocess.run([classifier_path, f], capture_output=True, text=True)
        out = result.stdout.strip()
        if result.returncode != 0 or out != "CLEAN":
            modified_clean.append(os.path.basename(f))

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))