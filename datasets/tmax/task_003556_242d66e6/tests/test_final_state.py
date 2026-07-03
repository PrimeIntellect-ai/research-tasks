# test_final_state.py

import os
import re
import difflib
import pytest

def test_ingest_log_metric():
    """
    Verify that the ingest.log file exists, contains the correct format,
    and the transcribed text matches the expected ground truth with >= 0.80 similarity.
    """
    log_file = "/home/user/ingest.log"
    assert os.path.exists(log_file), f"Expected log file {log_file} does not exist. Did the git hook run successfully?"

    with open(log_file, "r") as f:
        content = f.read().strip()

    # Check for the expected format
    match = re.search(r"Transcript:\s*(.*)", content)
    assert match is not None, "Could not find 'Transcript: <text>' in ingest.log. Ensure the git hook writes strictly in the requested format."

    actual = match.group(1).lower().strip()
    actual_clean = re.sub(r'[^a-z0-9\s]', '', actual)

    expected = "the temperature sensor on unit four is malfunctioning".lower()
    expected_clean = re.sub(r'[^a-z0-9\s]', '', expected)

    score = difflib.SequenceMatcher(None, expected_clean, actual_clean).ratio()

    assert score >= 0.80, f"Transcript similarity score {score:.3f} is below the 0.80 threshold. Actual transcript extracted: '{actual}'"

def test_owner_extracted_correctly():
    """
    Verify that the owner was correctly extracted from the metadata.txt and logged.
    """
    log_file = "/home/user/ingest.log"
    if not os.path.exists(log_file):
        pytest.fail(f"Expected log file {log_file} does not exist.")

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert "Owner: edge_device_alpha" in content, "The correct owner 'edge_device_alpha' was not found in ingest.log. Ensure the git hook extracts it properly."

def test_bare_repo_exists():
    """
    Verify that the bare git repository was created.
    """
    repo_dir = "/home/user/iot_ingest.git"
    assert os.path.isdir(repo_dir), f"Bare repository directory {repo_dir} does not exist."
    assert os.path.exists(os.path.join(repo_dir, "config")), "Repository does not appear to be initialized."

    # Check if it's a bare repo
    with open(os.path.join(repo_dir, "config"), "r") as f:
        config_content = f.read()
    assert "bare = true" in config_content.lower(), f"Repository at {repo_dir} is not configured as a bare repository."

def test_python_script_exists():
    """
    Verify that the processing python script exists.
    """
    script_path = "/home/user/process_audio.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."