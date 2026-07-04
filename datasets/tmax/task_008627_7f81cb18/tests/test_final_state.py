# test_final_state.py

import os
import sys
import subprocess
import pytest

def get_expected_result():
    """
    Computes the expected ground truth by running a subprocess that uses numpy.
    This avoids importing third-party libraries directly in the test file.
    """
    script = """
import numpy as np
np.random.seed(42)
seq = "".join(np.random.choice(['A', 'C', 'G', 'T'], size=1000000))
chunk_size = 50000
chunks = [(i, seq[i:i+chunk_size]) for i in range(0, len(seq), chunk_size)]

results = []
for idx, chunk in chunks:
    gc_counts = np.array([1.1 if b in 'GC' else 0.9 for b in chunk])
    cum_gc = np.cumsum(gc_counts)
    integral = np.trapz(np.sin(cum_gc))
    results.append(integral)

expected_total = sum(results)
print(f"{expected_total:.12f}")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_final_result_exists():
    """Check that the final_result.txt file was created."""
    result_path = "/home/user/final_result.txt"
    assert os.path.isfile(result_path), f"The file {result_path} does not exist. Did the script run successfully?"

def test_script_fixed():
    """Check that the script no longer uses imap_unordered."""
    script_path = "/home/user/integrate_mutation.py"
    with open(script_path, 'r') as f:
        content = f.read()

    assert "imap_unordered" not in content, "The script still contains 'imap_unordered'. You must use a sequential combination method (like imap or map)."

def test_final_result_correctness():
    """Check that the final_result.txt contains the exact expected float value."""
    result_path = "/home/user/final_result.txt"

    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    expected_result = get_expected_result()

    assert actual_result == expected_result, (
        f"The result in {result_path} is incorrect.\n"
        f"Expected: {expected_result}\n"
        f"Actual:   {actual_result}\n"
        "Ensure that you are summing the chunks in strict sequential order."
    )