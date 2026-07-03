# test_final_state.py
import os
import sys
import glob
import time
import pytest

BASE_DIR = "/home/user/release_prep"
SRC_DIR = os.path.join(BASE_DIR, "src")

def test_c_extension_compiled():
    """Verify that the C extension was successfully compiled."""
    so_files = glob.glob(os.path.join(BASE_DIR, "token_validator.*.so"))
    assert len(so_files) > 0, "The C extension token_validator.*.so was not found in the base directory. Did you fix setup.py and run build_ext?"

def test_setup_py_fixed():
    """Verify that setup.py includes the math library linkage."""
    setup_file = os.path.join(BASE_DIR, "setup.py")
    assert os.path.isfile(setup_file), "setup.py is missing."
    with open(setup_file, "r") as f:
        content = f.read()
    assert "libraries" in content and "'m'" in content.replace('"', "'"), "setup.py does not seem to link the math library (libraries=['m'])."

def test_app_rate_limiting_and_history():
    """Verify rate limiting and memory leak fix in app.py."""
    sys.path.insert(0, SRC_DIR)
    try:
        import app
    except ImportError:
        pytest.fail("Could not import app.py")

    # Check for custom exception
    assert hasattr(app, "RateLimitExceeded"), "RateLimitExceeded exception is not defined in app.py"
    RateLimitExceeded = app.RateLimitExceeded

    # Test history bound (memory leak fix)
    app.HISTORY = ["old"] * 100
    try:
        app.process_request("new_token")
    except RateLimitExceeded:
        pass

    assert len(app.HISTORY) <= 20, f"Memory leak not fixed: HISTORY list size is {len(app.HISTORY)}, expected <= 20"

    # Test rate limiter logic
    app.HISTORY = []
    success_count = 0
    exception_count = 0

    # Sleep briefly to ensure a fresh time window if previous tests messed with it
    time.sleep(1.1)

    for _ in range(10):
        try:
            app.process_request("test_token")
            success_count += 1
        except RateLimitExceeded:
            exception_count += 1

    assert success_count == 5, f"Rate limiter allowed {success_count} requests, expected exactly 5."
    assert exception_count == 5, f"Rate limiter raised exception {exception_count} times, expected exactly 5."

def test_verification_script_results():
    """Verify the output of the test script."""
    results_file = os.path.join(BASE_DIR, "test_results.txt")
    assert os.path.isfile(results_file), "test_results.txt was not created."

    with open(results_file, "r") as f:
        content = f.read().strip()

    assert "Successful: 5" in content, f"test_results.txt does not contain 'Successful: 5'. Content: {content}"
    assert "History Size:" in content, f"test_results.txt does not contain 'History Size:'. Content: {content}"