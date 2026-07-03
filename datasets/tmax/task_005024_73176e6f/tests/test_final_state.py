# test_final_state.py

import os
import re
import pytest

def test_gitlab_ci_exists():
    """Test that the .gitlab-ci.yml file was generated."""
    assert os.path.exists("/home/user/.gitlab-ci.yml"), "/home/user/.gitlab-ci.yml was not generated."

def test_gitlab_ci_stages():
    """Test that the stages are correctly defined in .gitlab-ci.yml."""
    with open("/home/user/.gitlab-ci.yml", "r") as f:
        content = f.read()

    # Extract stages block
    stages_match = re.search(r'^stages:\s*\n((?:\s*-\s*stage_\d+\s*\n)+)', content, re.MULTILINE)
    assert stages_match is not None, "Could not find a valid 'stages:' array in the YAML."

    stages_block = stages_match.group(1)
    stages = re.findall(r'-\s*(stage_\d+)', stages_block)

    expected_stages = ["stage_0", "stage_1", "stage_2", "stage_3"]
    assert stages == expected_stages, f"Expected stages {expected_stages}, but got {stages}."

def test_gitlab_ci_jobs():
    """Test that each job is correctly defined with its stage and script."""
    with open("/home/user/.gitlab-ci.yml", "r") as f:
        content = f.read()

    expected_jobs = {
        "auth": "stage_0",
        "db": "stage_0",
        "user": "stage_1",
        "notification": "stage_2",
        "payment": "stage_2",
        "gateway": "stage_3",
    }

    for job, expected_stage in expected_jobs.items():
        # Find the job block, stopping at the next top-level key or end of file
        block_pattern = rf'^build_{job}:\s*\n(.*?)(?=^\S|\Z)'
        match = re.search(block_pattern, content, re.MULTILINE | re.DOTALL)
        assert match is not None, f"Job block 'build_{job}:' not found."

        block = match.group(1)

        # Check stage
        stage_match = re.search(r'^\s+stage:\s*(stage_\d+)', block, re.MULTILINE)
        assert stage_match is not None, f"'stage:' missing in 'build_{job}'."
        actual_stage = stage_match.group(1)
        assert actual_stage == expected_stage, f"Expected 'build_{job}' to be in {expected_stage}, got {actual_stage}."

        # Check script
        script_match = re.search(r'^\s+script:\s*\n\s*-\s*(.+)', block, re.MULTILINE)
        assert script_match is not None, f"'script:' array missing or malformed in 'build_{job}'."
        script_cmd = script_match.group(1).strip()

        # Allow optional quotes around the echo command, but strictly check the printed string
        expected_echo = f'echo "Building {job}"'
        assert expected_echo in script_cmd.replace("'", '"'), f"Expected script to contain '{expected_echo}' in 'build_{job}', got '{script_cmd}'."