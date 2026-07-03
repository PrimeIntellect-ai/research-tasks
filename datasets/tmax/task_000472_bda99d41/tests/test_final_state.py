# test_final_state.py
import os
import sys
import pytest

def test_vendored_package_fixed_and_installed():
    """Verify the mail-sender-v2 package was fixed and installed correctly."""
    try:
        import mail_sender
        import mail_sender.connection
    except ImportError as e:
        pytest.fail(f"Failed to import mail_sender. Ensure you ran pip install -e /app/vendored/mail-sender-v2. Error: {e}")

    # Ensure the environment doesn't have the old override variable
    if 'MAIL_PORT_OVERRIDE' in os.environ:
        del os.environ['MAIL_PORT_OVERRIDE']

    try:
        # The connect function should now use SMTP_PORT or fallback to 25
        result = mail_sender.connection.connect()
        assert result is not None, "connect() returned None"
    except KeyError as e:
        if 'MAIL_PORT_OVERRIDE' in str(e):
            pytest.fail("mail_sender/connection.py still references MAIL_PORT_OVERRIDE without a fallback.")
        else:
            pytest.fail(f"mail_sender.connection.connect() raised unexpected KeyError: {e}")
    except Exception as e:
        pytest.fail(f"mail_sender.connection.connect() raised unexpected Exception: {e}")

def test_path_checker_adversarial_corpus():
    """Verify the path_checker correctly classifies clean and evil paths."""
    checker_file = "/home/user/path_checker.py"
    assert os.path.isfile(checker_file), f"File {checker_file} is missing. You must create the path classifier."

    sys.path.insert(0, "/home/user")
    try:
        import path_checker
    except ImportError as e:
        pytest.fail(f"Failed to import path_checker: {e}")

    assert hasattr(path_checker, "is_safe_backup_path"), "is_safe_backup_path function is missing in path_checker.py"
    is_safe = path_checker.is_safe_backup_path

    clean_file = "/app/corpora/clean/paths.txt"
    evil_file = "/app/corpora/evil/paths.txt"

    assert os.path.isfile(clean_file), f"Clean corpus missing at {clean_file}"
    assert os.path.isfile(evil_file), f"Evil corpus missing at {evil_file}"

    with open(clean_file, "r") as f:
        clean_paths = f.read().splitlines()
    with open(evil_file, "r") as f:
        evil_paths = f.read().splitlines()

    clean_failures = []
    for p in clean_paths:
        try:
            if not is_safe(p):
                clean_failures.append(p)
        except Exception as e:
            pytest.fail(f"is_safe_backup_path raised an exception on clean path '{p}': {e}")

    evil_failures = []
    for p in evil_paths:
        try:
            if is_safe(p):
                evil_failures.append(p)
        except Exception as e:
            # If it raises an exception on evil input, it technically didn't return True, 
            # but it's better to fail gracefully. We'll count it as a failure to return False cleanly.
            pytest.fail(f"is_safe_backup_path raised an exception on evil path '{p}': {e}")

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_paths)} evil bypassed: {evil_failures}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_paths)} clean modified (rejected): {clean_failures}")

    if errors:
        pytest.fail(" | ".join(errors))