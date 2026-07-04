# test_final_state.py

import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/project"
MAKEFILE_PATH = os.path.join(PROJECT_DIR, "Makefile")
CI_YML_PATH = os.path.join(PROJECT_DIR, ".github", "workflows", "ci.yml")
CONFIG_PATH = os.path.join(PROJECT_DIR, "build_config.json")

def test_makefile_exists():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile is missing at {MAKEFILE_PATH}"

def test_ci_yml_exists_and_contents():
    assert os.path.isfile(CI_YML_PATH), f"GitHub Actions workflow missing at {CI_YML_PATH}"

    with open(CI_YML_PATH, 'r') as f:
        content = f.read()

    # Basic checks for required CI/CD components
    assert "push" in content and "main" in content, "Workflow must trigger on push to main branch."
    assert "ubuntu-latest" in content, "Workflow must run on ubuntu-latest."
    assert "actions/checkout@v3" in content, "Workflow must use actions/checkout@v3."
    assert "make all" in content, "Workflow must run 'make all'."

def test_makefile_structure():
    with open(MAKEFILE_PATH, 'r') as f:
        content = f.read()

    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    targets = config.get("targets", {})

    # Check for all target
    assert "all:" in content, "Makefile must contain an 'all' target."

    # Check dependencies and commands for each target
    for target_name, target_info in targets.items():
        assert f"{target_name}:" in content, f"Makefile missing rule for target: {target_name}"

        # Check prerequisites
        src = target_info["src"]
        assert src in content, f"Makefile rule for {target_name} must depend on {src}"
        for dep in target_info["deps"]:
            assert dep in content, f"Makefile rule for {target_name} must depend on {dep}"

        # Check commands
        if target_info["lang"] == "c":
            assert f"gcc {src} -o {target_name}" in content, f"Missing or incorrect compile command for {target_name}"
        else:
            assert f"cp {src} {target_name}" in content, f"Missing copy command for {target_name}"
            assert f"chmod +x {target_name}" in content, f"Missing chmod command for {target_name}"

def test_make_all_execution():
    # Run make all to verify it works
    try:
        subprocess.run(["make", "-B", "all"], cwd=PROJECT_DIR, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'make all' failed to execute correctly.\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

    # Verify executables were created
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    for target_name in config.get("targets", {}):
        target_path = os.path.join(PROJECT_DIR, target_name)
        assert os.path.isfile(target_path), f"Executable {target_name} was not created by make."
        assert os.access(target_path, os.X_OK), f"File {target_name} is not executable."