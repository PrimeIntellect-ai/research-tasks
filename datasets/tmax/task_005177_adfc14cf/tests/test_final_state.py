# test_final_state.py

import os
import subprocess
import pytest

def test_predictions_csv_content():
    """Check if predictions.csv exists and has the correct exact content."""
    predictions_path = '/home/user/risk_pipeline/predictions.csv'
    assert os.path.isfile(predictions_path), f"Error: {predictions_path} not found."

    expected_content = [
        "id,score",
        "1,2.525",
        "2,2.625",
        "3,0.550",
        "4,3.050",
        "5,0.810"
    ]

    with open(predictions_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_content, f"Content of {predictions_path} does not match the expected output."

def test_cargo_tests_pass():
    """Check if cargo test passes and contains test_reproducibility."""
    project_dir = '/home/user/risk_pipeline'
    assert os.path.isdir(project_dir), f"Error: Cargo project directory {project_dir} not found."

    try:
        result = subprocess.run(
            ['cargo', 'test'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
    except FileNotFoundError:
        pytest.fail("Error: 'cargo' command not found. Is Rust installed?")
    except subprocess.TimeoutExpired:
        pytest.fail("Error: 'cargo test' timed out.")

    assert result.returncode == 0, f"Error: Cargo tests failed.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert "test_reproducibility" in result.stdout or "test_reproducibility" in result.stderr, \
        "Error: 'test_reproducibility' not found in test execution output."