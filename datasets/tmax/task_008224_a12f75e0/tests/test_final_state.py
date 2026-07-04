# test_final_state.py

import os
import json
import pytest

PROJECT_DIR = "/home/user/release_manager"
FIXTURES_DIR = os.path.join(PROJECT_DIR, "fixtures")
CI_SCRIPT = os.path.join(PROJECT_DIR, "ci.sh")
CI_RESULTS = os.path.join(PROJECT_DIR, "ci_results.log")
RELEASE_BINARY = os.path.join(PROJECT_DIR, "target", "release", "release_checker")

def test_rust_binary_compiled():
    """Verify that the Rust project was compiled in release mode."""
    assert os.path.isfile(RELEASE_BINARY), (
        f"The release binary was not found at {RELEASE_BINARY}. "
        "Did you run 'cargo build --release' successfully?"
    )
    assert os.access(RELEASE_BINARY, os.X_OK), (
        f"The file at {RELEASE_BINARY} is not executable."
    )

def test_fixtures_exist_and_valid():
    """Verify that the test fixtures are created correctly with the specified content."""
    assert os.path.isdir(FIXTURES_DIR), f"Fixtures directory not found at {FIXTURES_DIR}"

    expected_fixtures = {
        "valid.json": {
            "version": "2.1.0",
            "data": "update_package_A",
            "checksum": "4027419ef9c2b48cd029fc12d592fba499ffdc7bde0991c28cde3c467a90f1d1"
        },
        "bad_checksum.json": {
            "version": "2.1.0",
            "data": "update_package_A",
            "checksum": "badbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadbadb"
        },
        "downgrade.json": {
            "version": "1.5.0",
            "data": "update_package_B",
            "checksum": "b80b2a32c25bc5e5108cc9c66af7e20ecba094de193c78d5312010fb09e7de7b"
        }
    }

    for filename, expected_data in expected_fixtures.items():
        filepath = os.path.join(FIXTURES_DIR, filename)
        assert os.path.isfile(filepath), f"Fixture file missing: {filepath}"

        with open(filepath, 'r') as f:
            try:
                actual_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"Fixture file {filepath} is not valid JSON.")

        assert actual_data == expected_data, (
            f"Content of {filepath} does not match expected values.\n"
            f"Expected: {expected_data}\nActual: {actual_data}"
        )

def test_ci_script_executable():
    """Verify that the CI script exists and is executable."""
    assert os.path.isfile(CI_SCRIPT), f"CI script not found at {CI_SCRIPT}"
    assert os.access(CI_SCRIPT, os.X_OK), f"CI script at {CI_SCRIPT} is not executable."

def test_ci_results_log():
    """Verify that the CI results log matches the expected output exactly."""
    assert os.path.isfile(CI_RESULTS), f"CI results log not found at {CI_RESULTS}"

    with open(CI_RESULTS, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "PASS",
        "FAIL: CHECKSUM",
        "FAIL: DOWNGRADE"
    ]

    assert lines == expected_lines, (
        f"The contents of {CI_RESULTS} do not match the expected output.\n"
        f"Expected: {expected_lines}\nActual: {lines}"
    )