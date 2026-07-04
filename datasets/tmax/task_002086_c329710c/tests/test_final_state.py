# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
INSTALL_PLAN_PATH = os.path.join(WORKSPACE_DIR, "install_plan.json")
GO_MOD_PATH = os.path.join(WORKSPACE_DIR, "go.mod")
SOLVER_GO_PATH = os.path.join(WORKSPACE_DIR, "solver.go")
SOLVER_TEST_GO_PATH = os.path.join(WORKSPACE_DIR, "solver_test.go")

def test_go_module_initialized():
    """Verify that the go.mod file exists and contains the correct module name."""
    assert os.path.isfile(GO_MOD_PATH), f"go.mod file is missing at {GO_MOD_PATH}"
    with open(GO_MOD_PATH, "r") as f:
        content = f.read()
    assert "module mathpack" in content, "go.mod does not declare the 'mathpack' module."

def test_go_files_exist():
    """Verify that solver.go and solver_test.go exist."""
    assert os.path.isfile(SOLVER_GO_PATH), f"solver.go is missing at {SOLVER_GO_PATH}"
    assert os.path.isfile(SOLVER_TEST_GO_PATH), f"solver_test.go is missing at {SOLVER_TEST_GO_PATH}"

def test_go_tests_pass():
    """Verify that 'go test' runs successfully in the workspace directory."""
    try:
        result = subprocess.run(
            ["go", "test"],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=15
        )
        assert result.returncode == 0, f"'go test' failed with output:\n{result.stdout}\n{result.stderr}"
    except FileNotFoundError:
        pytest.fail("The 'go' command is not available. Go might not be installed or in PATH.")
    except subprocess.TimeoutExpired:
        pytest.fail("'go test' timed out.")

def test_install_plan_json():
    """Verify that install_plan.json contains the correct list of packages."""
    assert os.path.isfile(INSTALL_PLAN_PATH), f"install_plan.json is missing at {INSTALL_PLAN_PATH}"

    with open(INSTALL_PLAN_PATH, "r") as f:
        try:
            plan = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{INSTALL_PLAN_PATH} does not contain valid JSON.")

    expected_plan = ["core-app", "libA", "plugin2", "util"]

    assert isinstance(plan, list), "install_plan.json should contain a JSON array."
    assert plan == expected_plan, f"install_plan.json does not match the expected output. Got {plan}, expected {expected_plan}."