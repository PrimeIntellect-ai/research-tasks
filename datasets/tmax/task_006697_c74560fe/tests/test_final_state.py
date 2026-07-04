# test_final_state.py

import os
import hashlib
import re
import pytest

def test_version_bumper_compiled():
    binary_path = "/home/user/artifact_manager/version_bumper"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist. Did you fix the Makefile and run make?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_scripts_executable():
    scripts = [
        "/home/user/artifact_manager/test_property.sh",
        "/home/user/artifact_manager/ci_pipeline.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_pipeline_report():
    report_path = "/home/user/artifact_manager/pipeline_report.txt"
    binary_path = "/home/user/artifact_manager/version_bumper"

    assert os.path.isfile(report_path), f"Report {report_path} does not exist. Did you run the CI pipeline script?"

    with open(report_path, 'r') as f:
        content = f.read().strip()

    match = re.match(r"^SUCCESS:\s*([a-f0-9]{64})$", content)
    assert match, f"Report content '{content}' does not match the expected format 'SUCCESS: <sha256_hash>'."

    reported_hash = match.group(1)

    with open(binary_path, 'rb') as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    assert reported_hash == actual_hash, f"Reported hash {reported_hash} does not match actual hash of the binary {actual_hash}."