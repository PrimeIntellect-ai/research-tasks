# test_final_state.py

import os
import subprocess
import random
import pytest
import sys

def test_pyproject_toml_valid():
    """Check if the pyproject.toml file is valid TOML."""
    toml_path = "/home/user/qa_project/pyproject.toml"
    assert os.path.isfile(toml_path), f"File {toml_path} is missing."

    if sys.version_info >= (3, 11):
        import tomllib
        with open(toml_path, "rb") as f:
            try:
                tomllib.load(f)
            except Exception as e:
                pytest.fail(f"pyproject.toml is still invalid TOML: {e}")
    else:
        # If older python, just check it has basic valid content (e.g. no obvious syntax errors)
        # The agent's task was to fix syntax errors.
        with open(toml_path, "r") as f:
            content = f.read()
        assert "name =" in content or "name=" in content, "pyproject.toml seems to be missing basic metadata."

def test_run_e2e_tests_updated():
    """Verify that the orchestrator script has been updated to use the new bash script."""
    path = "/home/user/qa_project/run_e2e_tests.sh"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "/app/legacy_resolver" not in content, "run_e2e_tests.sh still references the legacy binary /app/legacy_resolver."
    assert "semver_match.sh" in content, "run_e2e_tests.sh does not reference the new semver_match.sh script."

def test_semver_match_accuracy():
    """Test the accuracy of the new bash replacement against the legacy binary."""
    script_path = "/home/user/semver_match.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    def generate_test_cases(num=200):
        cases = []
        versions = ["1.0.0", "1.2.3", "2.0.0-rc1", "0.9.9", "3.4.5"]
        ops = [">", "<", ">=", "<=", "=", "!="]
        bools = ["&&", "||"]
        random.seed(42) # Fixed seed for reproducible tests
        for _ in range(num):
            v = random.choice(versions)
            expr = f"{random.choice(ops)}{random.choice(versions)} {random.choice(bools)} {random.choice(ops)}{random.choice(versions)}"
            if random.random() > 0.5:
                expr = f"({expr}) {random.choice(bools)} {random.choice(ops)}{random.choice(versions)}"
            cases.append((expr, v))
        return cases

    matches = 0
    cases = generate_test_cases(200)

    for expr, v in cases:
        try:
            ref_code = subprocess.run(["/app/legacy_resolver", expr, v], capture_output=True).returncode
        except Exception:
            ref_code = -1

        try:
            test_code = subprocess.run(["bash", script_path, expr, v], capture_output=True, timeout=1).returncode
        except subprocess.TimeoutExpired:
            test_code = -2
        except Exception:
            test_code = -3

        # Normalize exit codes to boolean (0 is success/true, non-zero is failure/false)
        if (ref_code == 0 and test_code == 0) or (ref_code != 0 and test_code != 0):
            matches += 1

    accuracy = matches / len(cases)
    assert accuracy >= 0.95, f"Accuracy {accuracy:.2f} is below the 0.95 threshold. The script did not match the legacy resolver behavior closely enough."