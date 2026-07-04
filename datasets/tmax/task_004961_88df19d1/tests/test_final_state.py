# test_final_state.py

import os
import sys

def test_success_log_exists_and_correct():
    """Test that success.log was generated and contains the correct output."""
    log_path = "/home/user/app/success.log"
    assert os.path.isfile(log_path), "The file /home/user/app/success.log does not exist. Did you run verify.py?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "Fixed: 100000000.0, 0.0", f"success.log contains incorrect output: {content}"

def test_processor_fix_robustness():
    """Test that compute_statistics actually fixes the numerical instability."""
    sys.path.insert(0, "/home/user/app")
    try:
        from processor import compute_statistics
    except ImportError:
        raise AssertionError("Could not import compute_statistics from /home/user/app/processor.py")
    finally:
        sys.path.pop(0)

    # Test the specific edge case that caused the crash
    data = [100000000.0, 100000000.0, 100000000.0]
    try:
        mean, stddev = compute_statistics(data)
    except ValueError as e:
        raise AssertionError(f"compute_statistics still crashes with ValueError: {e}")

    assert mean == 100000000.0, f"Expected mean 100000000.0, got {mean}"
    assert stddev == 0.0, f"Expected stddev 0.0, got {stddev}"

    # Test normal data to ensure it still works
    normal_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    mean, stddev = compute_statistics(normal_data)
    assert mean == 3.0, f"Expected mean 3.0, got {mean}"
    # Population stddev of [1, 2, 3, 4, 5] is sqrt(2) ~ 1.41421356
    assert abs(stddev - 1.41421356) < 1e-5, f"Expected stddev ~1.414, got {stddev}"