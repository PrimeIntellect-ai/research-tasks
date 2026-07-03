# test_final_state.py

import os
import subprocess
import pytest

def test_scanner_executable_exists():
    scanner_path = "/home/user/scanner"
    assert os.path.exists(scanner_path), f"Agent's scanner binary is missing at {scanner_path}"
    assert os.path.isfile(scanner_path), f"{scanner_path} is not a file"
    assert os.access(scanner_path, os.X_OK), f"Agent's scanner at {scanner_path} is not executable"

def test_scanner_accuracy():
    scanner_path = "/home/user/scanner"
    legacy_path = "/app/legacy_scanner"
    hidden_test_file = "/test_data/hidden_logs.txt"

    assert os.path.exists(legacy_path), f"Legacy scanner missing at {legacy_path}"
    assert os.path.exists(hidden_test_file), f"Hidden test file missing at {hidden_test_file}"

    # Run agent scanner
    try:
        agent_out = subprocess.check_output([scanner_path, hidden_test_file], text=True).strip().split('\n')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent's scanner failed to execute: {e}")
    except Exception as e:
        pytest.fail(f"Error running agent's scanner: {e}")

    # Run legacy scanner
    try:
        legacy_out = subprocess.check_output([legacy_path, hidden_test_file], text=True).strip().split('\n')
    except Exception as e:
        pytest.fail(f"Error running legacy scanner: {e}")

    assert len(agent_out) > 0, "Agent's scanner produced no output."
    assert len(agent_out) == len(legacy_out), f"Output length mismatch: agent produced {len(agent_out)} lines, expected {len(legacy_out)} lines."

    matches = sum(1 for a, b in zip(agent_out, legacy_out) if a.strip() == b.strip())
    accuracy = matches / len(legacy_out)

    assert accuracy >= 1.0, f"Accuracy is {accuracy}, expected 1.0. The agent's scanner output does not perfectly match the legacy scanner."