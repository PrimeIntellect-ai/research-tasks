# test_final_state.py

import os
import subprocess
import pytest

def test_build_script_exists():
    """Verify that the build script exists."""
    script_path = "/home/user/project/build.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_build_script_execution_and_artifact():
    """
    Run the build script to ensure it no longer crashes and 
    generates the correct artifact file.
    """
    script_path = "/home/user/project/build.py"
    artifact_path = "/home/user/project/build_artifact.txt"

    # Run the script
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    # Check that the script executed successfully
    assert result.returncode == 0, (
        f"The script {script_path} failed with exit code {result.returncode}.\n"
        f"Standard Error:\n{result.stderr}"
    )

    # Check that the artifact was generated
    assert os.path.isfile(artifact_path), (
        f"The artifact file {artifact_path} was not created after running the script. "
        "The script might still have a bug causing premature file deletion."
    )

    # Check the contents of the artifact
    with open(artifact_path, "r") as f:
        content = f.read().strip()

    expected_content = "SUCCESS: 1.0.42"
    assert content == expected_content, (
        f"The artifact file {artifact_path} does not contain the expected text. "
        f"Expected '{expected_content}', but got '{content}'."
    )