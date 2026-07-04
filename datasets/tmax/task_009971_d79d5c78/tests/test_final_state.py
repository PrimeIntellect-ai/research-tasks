# test_final_state.py
import os
import subprocess
import pytest

def test_c_source_exists():
    assert os.path.isfile('/home/user/graph_query.c'), "C source file /home/user/graph_query.c is missing."

def test_binary_exists_and_executable():
    assert os.path.isfile('/home/user/graph_query'), "Compiled binary /home/user/graph_query is missing."
    assert os.access('/home/user/graph_query', os.X_OK), "/home/user/graph_query is not executable."

def test_results_match():
    # Run the binary if results.csv doesn't exist, or to ensure it's up to date.
    if not os.path.isfile('/home/user/results.csv'):
        try:
            subprocess.run(['/home/user/graph_query'], cwd='/home/user', capture_output=True, timeout=15, check=True)
        except subprocess.TimeoutExpired:
            pytest.fail("The C program timed out. It must be optimized.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"The C program failed to execute: {e.stderr.decode('utf-8', errors='ignore')}")

    assert os.path.isfile('/home/user/results.csv'), "/home/user/results.csv was not generated."

    with open('/home/user/results.csv', 'r') as f:
        results = [line.strip() for line in f if line.strip()]

    with open('/home/user/expected_results.csv', 'r') as f:
        expected = [line.strip() for line in f if line.strip()]

    assert sorted(results) == sorted(expected), "The generated results in /home/user/results.csv do not match the expected results."