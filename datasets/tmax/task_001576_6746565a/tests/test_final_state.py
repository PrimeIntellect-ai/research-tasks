# test_final_state.py
import os
import sys
import time
import importlib.util

def test_circular_import_fixed():
    """Verify that models.py can be imported without ImportError."""
    sys.path.insert(0, '/home/user/dataproc')
    try:
        import models
        import validator
    except ImportError as e:
        assert False, f"ImportError still present: {e}"
    finally:
        if '/home/user/dataproc' in sys.path:
            sys.path.remove('/home/user/dataproc')

def test_rate_limiting_logic():
    """Verify the rate limiter allows 3 requests per second per client_id."""
    sys.path.insert(0, '/home/user/dataproc')
    try:
        import validator
        importlib.reload(validator) # Ensure clean state if previously imported
    except ImportError:
        assert False, "Could not import validator.py"
    finally:
        if '/home/user/dataproc' in sys.path:
            sys.path.remove('/home/user/dataproc')

    client_id = "test_client_final"
    results = [validator.rate_limit_check(client_id) for _ in range(5)]
    assert results == [True, True, True, False, False], f"Rate limiting failed for 5 rapid requests. Got {results}"

    time.sleep(1.1)
    assert validator.rate_limit_check(client_id) is True, "Rate limiting failed to reset after 1 second."

def test_test_results_log_exists_and_passed():
    """Verify that test_results.log exists and contains passing output."""
    log_path = '/home/user/test_results.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    assert "test_models.py" in content, "test_results.log does not mention test_models.py."
    assert "passed" in content or "1 passed" in content, "test_results.log does not indicate a passed test."

def test_hypothesis_test_implemented():
    """Verify test_models.py contains the required hypothesis test and decorator."""
    test_file_path = '/home/user/dataproc/test_models.py'
    assert os.path.exists(test_file_path), f"{test_file_path} does not exist."

    with open(test_file_path, 'r') as f:
        content = f.read()

    assert "test_event_serialization_symmetry" in content, "test_event_serialization_symmetry not found in test_models.py."
    assert "@given" in content, "@given decorator not found in test_models.py."