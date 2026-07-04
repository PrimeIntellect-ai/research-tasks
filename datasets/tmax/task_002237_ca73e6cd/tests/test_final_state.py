# test_final_state.py

import time
import subprocess
import os
import pytest

legacy_bin = "/app/legacy_resolver"
fast_bin = "/home/user/fast_resolver"
test_dir = "/app/hidden_test_graphs"

def test_fast_resolver_exists():
    """Check that the fast resolver binary was compiled and is executable."""
    assert os.path.isfile(fast_bin), f"Fast resolver binary {fast_bin} does not exist. Did you compile it?"
    assert os.access(fast_bin, os.X_OK), f"Fast resolver binary {fast_bin} is not executable."

def test_accuracy_and_speedup():
    """Evaluate the accuracy and speedup of the fast resolver against the legacy binary."""
    assert os.path.isdir(test_dir), f"Test directory {test_dir} does not exist."
    test_files = [f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]
    assert len(test_files) > 0, "No test graphs found."

    correct = 0
    total = 0
    legacy_time = 0.0
    fast_time = 0.0

    for filename in test_files:
        filepath = os.path.join(test_dir, filename)

        t0 = time.time()
        try:
            leg_out = subprocess.check_output([legacy_bin, filepath], text=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            leg_out = e.output
        t1 = time.time()
        legacy_time += (t1 - t0)

        t0 = time.time()
        try:
            fast_out = subprocess.check_output([fast_bin, filepath], text=True, timeout=5.0, stderr=subprocess.STDOUT)
        except subprocess.TimeoutExpired:
            fast_out = "TIMEOUT"
        except subprocess.CalledProcessError as e:
            fast_out = e.output
        except Exception:
            fast_out = "ERROR"
        t1 = time.time()
        fast_time += (t1 - t0)

        if leg_out.strip() == fast_out.strip():
            correct += 1
        total += 1

    accuracy = correct / total
    speedup = legacy_time / fast_time if fast_time > 0 else 0.0

    assert accuracy >= 1.0, f"Accuracy is {accuracy*100:.2f}%, expected 100.0% match with legacy resolver."
    assert speedup >= 20.0, f"Speedup is {speedup:.2f}x, expected at least 20.0x."