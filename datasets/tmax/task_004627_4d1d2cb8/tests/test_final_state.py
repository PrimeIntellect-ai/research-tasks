# test_final_state.py

import os
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/audit_resolver.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_yaml_exists():
    yaml_path = "/home/user/.github/workflows/secure_build.yml"
    assert os.path.isfile(yaml_path), f"The generated workflow file {yaml_path} does not exist."

def test_yaml_content():
    yaml_path = "/home/user/.github/workflows/secure_build.yml"
    if not os.path.isfile(yaml_path):
        pytest.fail(f"Workflow file {yaml_path} missing, cannot check content.")

    with open(yaml_path, 'r') as f:
        content = f.read()

    # Check for the required versions as derived from the logic:
    # core-lib 1.0.0 is tampered, so we must use 1.1.0
    # web-framework 2.1.0 depends on core-lib 1.1.0
    # auth-plugin 3.0.0 depends on web-framework 2.1.0

    assert re.search(r"CORE_VERSION:\s*1\.1\.0", content), "CORE_VERSION is not correctly resolved to 1.1.0"
    assert re.search(r"WEB_VERSION:\s*2\.1\.0", content), "WEB_VERSION is not correctly resolved to 2.1.0"
    assert re.search(r"AUTH_VERSION:\s*3\.0\.0", content), "AUTH_VERSION is not correctly resolved to 3.0.0"

    # Check that the rest of the template is intact
    assert "name: Secure Build" in content, "Missing 'name: Secure Build' in YAML."
    assert "on: [push]" in content, "Missing 'on: [push]' in YAML."
    assert "runs-on: ubuntu-latest" in content, "Missing 'runs-on: ubuntu-latest' in YAML."
    assert "uses: actions/checkout@v3" in content, "Missing checkout step in YAML."
    assert "run: ./install.sh $CORE_VERSION $WEB_VERSION $AUTH_VERSION" in content, "Missing or incorrect install step in YAML."