# test_final_state.py

import os
import pytest

def test_speedup_metric():
    speedup_file = "/app/speedup.txt"

    # Check if the output file exists
    assert os.path.isfile(speedup_file), f"Expected output file not found: {speedup_file}"

    # Read the speedup value
    try:
        with open(speedup_file, "r") as f:
            content = f.read().strip()
            speedup = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {speedup_file} as a float. Content: '{content}'")
    except Exception as e:
        pytest.fail(f"Failed to read {speedup_file}: {e}")

    # Define the threshold
    threshold = 5.0

    # Assert the metric against the threshold
    assert speedup >= threshold, (
        f"Performance speedup {speedup:.2f}x is less than the required threshold of {threshold}x. "
        "Ensure your C implementation is fully optimized and correctly integrated."
    )

def test_shared_library_exists():
    so_file = "/app/libratelimit.so"
    assert os.path.isfile(so_file), f"Expected shared library not found: {so_file}. Ensure the Makefile builds it correctly."