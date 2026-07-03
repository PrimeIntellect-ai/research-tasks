# test_final_state.py

import os
import pytest

def test_manifest_stage1_updated():
    filepath = "/home/user/manifests/stage1.yaml"
    assert os.path.isfile(filepath), f"{filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()
    assert "image: myregistry.local/frontend:v2.0" in content, f"{filepath} was not updated to v2.0"
    assert "image: myregistry.local/frontend:v1.0" not in content, f"{filepath} still contains v1.0"

def test_manifest_stage2_updated():
    filepath = "/home/user/manifests/stage2.yaml"
    assert os.path.isfile(filepath), f"{filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()
    assert "image: myregistry.local/frontend:v2.0" in content, f"{filepath} was not updated to v2.0"
    assert "image: myregistry.local/frontend:v1.0" not in content, f"{filepath} still contains v1.0"

def test_manifest_stage3_unchanged():
    filepath = "/home/user/manifests/stage3.yaml"
    assert os.path.isfile(filepath), f"{filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()
    assert "image: myregistry.local/frontend:v1.0" in content, f"{filepath} was incorrectly updated. It should remain v1.0"
    assert "image: myregistry.local/frontend:v2.0" not in content, f"{filepath} should not contain v2.0 due to health check failure"

def test_deployment_email_content():
    filepath = "/home/user/deployment_email.eml"
    assert os.path.isfile(filepath), f"{filepath} was not generated"

    expected_content = (
        "To: devops-alerts@local.domain\n"
        "Subject: Staged Deployment Report\n\n"
        "Successful Deployments: stage1, stage2\n"
        "Failed Stage: stage3"
    ).strip()

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {filepath} does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"