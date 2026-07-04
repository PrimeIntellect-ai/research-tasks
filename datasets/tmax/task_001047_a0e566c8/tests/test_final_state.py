# test_final_state.py

import os
import subprocess
import sys
import random
import string
import pytest

def test_custom_session_lib_installed():
    """Check if the custom_session_lib was fixed and installed successfully."""
    try:
        import custom_session_lib
    except ImportError:
        pytest.fail("custom_session_lib is not installed in the current environment. Ensure you fixed setup.py and ran pip install.")

def test_forge_py_exists():
    """Check if the forge.py script exists at the correct location."""
    assert os.path.isfile("/home/user/forge.py"), "/home/user/forge.py does not exist."

def test_forge_py_accuracy():
    """
    Test the forge.py script against 50 random usernames.
    It must achieve a 1.0 accuracy (50/50 correct tokens).
    """
    try:
        import custom_session_lib
    except ImportError:
        pytest.fail("Cannot run accuracy test because custom_session_lib is not installed.")

    correct_count = 0
    total_cases = 50
    key = "secret42"

    for _ in range(total_cases):
        # Generate a random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

        try:
            # Run the student's script
            result = subprocess.run(
                [sys.executable, "/home/user/forge.py", username],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                continue

            token = result.stdout.strip()

            # The expected plaintext
            expected_plaintext = f"username:{username},role:admin"

            # Re-derive the expected token using the known key and algorithm
            expected_token = "".join(f"{ord(c) ^ ord(key[i % len(key)]):02x}" for i, c in enumerate(expected_plaintext))

            # Verify the token is correct
            is_valid = False

            # Try to use the library's verification function as described in the task
            try:
                if hasattr(custom_session_lib, 'verify_token'):
                    is_valid = custom_session_lib.verify_token(token)
            except Exception:
                is_valid = False

            # Fallback to exact match if verify_token behaves unexpectedly or to strictly enforce the crypto
            if token == expected_token:
                is_valid = True

            if is_valid:
                correct_count += 1

        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass

    accuracy = correct_count / float(total_cases)

    assert accuracy >= 1.0, (
        f"Metric threshold failed: Accuracy = {accuracy} (Threshold >= 1.0). "
        f"Only {correct_count} out of {total_cases} tokens were forged and validated correctly."
    )