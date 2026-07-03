# test_final_state.py

import os
import re
import subprocess
import pytest

BASE_DIR = "/home/user/release_prep"

def test_release_env_content():
    env_file = os.path.join(BASE_DIR, "release.env")
    assert os.path.isfile(env_file), f"{env_file} does not exist."

    with open(env_file, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "SERVICE_NAME=deployment-orchestrator",
        "ENVIRONMENT=production",
        "RELEASE_VERSION=v1.4.2"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    for expected in expected_lines:
        assert expected in actual_lines, f"Expected '{expected}' not found in {env_file}"

def test_service_proto_updated():
    proto_file = os.path.join(BASE_DIR, "service.proto")
    assert os.path.isfile(proto_file), f"{proto_file} does not exist."

    with open(proto_file, "r") as f:
        content = f.read()

    # Remove all whitespace to make matching robust against formatting differences
    stripped_content = re.sub(r'\s+', '', content)

    assert "messageHealthCheckResponse{" in stripped_content, "HealthCheckResponse message is missing or incorrectly formatted."
    assert "boolhealthy=1;" in stripped_content, "Field 'bool healthy = 1;' is missing in HealthCheckResponse."
    assert "rpcHealthCheck(google.protobuf.Empty)returns(HealthCheckResponse);" in stripped_content, "rpc HealthCheck definition is missing or incorrect."

def test_makefile_and_executable():
    makefile_orig = os.path.join(BASE_DIR, "Makefile.orig")
    makefile = os.path.join(BASE_DIR, "Makefile")
    executable = os.path.join(BASE_DIR, "check_util")

    assert os.path.isfile(makefile_orig), f"Backup file {makefile_orig} does not exist."
    assert os.path.isfile(makefile), f"Makefile {makefile} does not exist."

    with open(makefile, "r") as f:
        makefile_content = f.read()

    assert "-lm" in makefile_content, "Makefile does not link the math library (-lm)."

    assert os.path.isfile(executable), f"Executable {executable} does not exist. Did you run make?"
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

    result = subprocess.run([executable], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {executable} failed."
    assert "Validation complete. Status: 4.0" in result.stdout, f"Unexpected output from {executable}: {result.stdout}"

def test_makefile_patch():
    patch_file = os.path.join(BASE_DIR, "makefile_fix.patch")
    assert os.path.isfile(patch_file), f"Patch file {patch_file} does not exist."

    with open(patch_file, "r") as f:
        content = f.read()

    assert re.search(r'^---\s+Makefile\.orig', content, re.MULTILINE), f"{patch_file} does not look like a valid unified diff (missing '--- Makefile.orig')."
    assert re.search(r'^\+\+\+\s+Makefile', content, re.MULTILINE), f"{patch_file} does not look like a valid unified diff (missing '+++ Makefile')."
    assert re.search(r'^@@\s+', content, re.MULTILINE), f"{patch_file} does not contain diff hunks (missing '@@')."