# test_final_state.py
import os
import struct
import pytest

SOLUTION_FILE = "/home/user/solution.txt"
SHADOW_NUMPY = "/home/user/suspicious_repo/numpy.py"

def to_f32(val):
    """Simulate numpy.float32 precision using standard library struct."""
    return struct.unpack('f', struct.pack('f', val))[0]

def compute_expected_truth():
    seed = 0.123456789
    x32 = to_f32(seed)
    x64 = float(seed)

    idx = -1
    for i in range(100):
        # The numpy code does: x = np.float32(3.9) * x * (np.float32(1.0) - x)
        # Note: In the original script, it's np.float32(1.0) - x. 
        # When x is float32, the result of subtraction is float32.
        # Then it's multiplied by np.float32(3.9) and x.
        term1 = to_f32(3.9)
        term2 = to_f32(1.0)

        # Operations in numpy with float32 yield float32
        sub_res = to_f32(term2 - x32)
        mul1 = to_f32(term1 * x32)
        x32 = to_f32(mul1 * sub_res)

        x64 = 3.9 * x64 * (1.0 - x64)

        if abs(x32 - x64) > 0.5:
            idx = i
            break

    return seed, idx

def test_shadow_numpy_removed():
    assert not os.path.exists(SHADOW_NUMPY), (
        f"The shadow numpy file {SHADOW_NUMPY} still exists. "
        "The environment misconfiguration has not been fixed."
    )

def test_solution_file_exists():
    assert os.path.isfile(SOLUTION_FILE), (
        f"Solution file {SOLUTION_FILE} does not exist."
    )

def test_solution_content():
    seed, expected_idx = compute_expected_truth()

    with open(SOLUTION_FILE, "r") as f:
        content = f.read().strip()

    expected_seed_line = f"SEED: {seed}"
    expected_idx_line = f"DIVERGENCE_INDEX: {expected_idx}"

    assert expected_seed_line in content, (
        f"Could not find the correct SEED line in {SOLUTION_FILE}. "
        f"Expected to find '{expected_seed_line}'."
    )

    assert expected_idx_line in content, (
        f"Could not find the correct DIVERGENCE_INDEX line in {SOLUTION_FILE}. "
        f"Expected to find '{expected_idx_line}'."
    )