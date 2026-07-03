# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/resolve_build.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_build_plan_correct():
    plan_path = "/home/user/build_plan.txt"
    assert os.path.isfile(plan_path), f"Build plan {plan_path} does not exist."

    with open(plan_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = [
        "base.tar",
        "crypto.so",
        "net.so",
        "backend.bin",
        "frontend.bin",
        "release.zip"
    ]

    assert lines == expected_order, f"Build plan order is incorrect. Expected {expected_order}, got {lines}."

def test_script_behavior_on_checksum_failure():
    script_path = "/home/user/resolve_build.sh"
    artifact_path = "/home/user/artifacts/backend.bin"

    assert os.path.isfile(artifact_path), f"Artifact {artifact_path} is missing."

    # Backup original content
    with open(artifact_path, "rb") as f:
        original_content = f.read()

    try:
        # Corrupt the artifact to cause a checksum mismatch
        with open(artifact_path, "wb") as f:
            f.write(b"corrupted_content_for_test")

        # Run the script
        result = subprocess.run([script_path], capture_output=True, text=True)

        assert result.returncode == 1, f"Expected script to exit with status 1 on checksum failure, but got {result.returncode}."
        assert "ERROR: backend.bin" in result.stdout, f"Expected 'ERROR: backend.bin' in stdout, but got: {result.stdout}"
    finally:
        # Restore original content
        with open(artifact_path, "wb") as f:
            f.write(original_content)