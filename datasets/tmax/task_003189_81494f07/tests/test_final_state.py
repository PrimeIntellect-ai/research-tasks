# test_final_state.py

import os
import json
import math
import subprocess
import pytest

PROJECT_DIR = "/home/user/model_fit"
LOG_FILE = "/home/user/integration_log.json"

def test_rust_project_exists():
    """Verify that the Rust project directory and Cargo.toml exist."""
    assert os.path.isdir(PROJECT_DIR), f"Rust project directory {PROJECT_DIR} does not exist."
    cargo_toml = os.path.join(PROJECT_DIR, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}."

def test_rust_project_compiles_and_runs():
    """Verify that the Rust project compiles and runs successfully."""
    # Remove the log file if it exists to ensure the run generates a new one
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    result = subprocess.run(
        ["cargo", "run"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"cargo run failed with exit code {result.returncode}.\nStderr: {result.stderr}"

def test_integration_log_exists():
    """Verify that the integration log file is generated."""
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not generated."

def test_integration_log_contents():
    """Verify the contents of the integration log file."""
    with open(LOG_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {LOG_FILE}")

    for key in ['analytical', 'numerical', 'error']:
        assert key in data, f"Key '{key}' missing from JSON output."
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

    analytical = data['analytical']
    numerical = data['numerical']
    error = data['error']

    expected_analytical = 2.0 * math.asinh(1.0 / 1e-4)

    assert abs(analytical - expected_analytical) < 1e-8, f"Analytical solution incorrect. Expected ~{expected_analytical}, got {analytical}."
    assert abs(abs(analytical - numerical) - error) < 1e-8, f"Error calculation incorrect. Expected {abs(analytical - numerical)}, got {error}."
    assert error < 1e-4, f"Numerical integration error is too high ({error}). Mesh refinement not implemented correctly."