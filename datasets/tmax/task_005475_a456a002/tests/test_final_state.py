# test_final_state.py
import os

def test_verification_log_exists_and_correct():
    path = "/home/user/auth_service/verification.log"
    assert os.path.isfile(path), f"Log file {path} is missing. The agent did not create the verification log."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "OLD_TOKEN_VALID: 302 | /home",
        "NEW_TOKEN_VALID: 302 | /settings",
        "OPEN_REDIRECT_BLOCKED: 302 | /dashboard"
    ]

    # Check that each expected line is in the log file
    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {path}. The verification log is incomplete or incorrectly formatted."

def test_auth_c_modifications():
    path = "/home/user/auth_service/auth.c"
    assert os.path.isfile(path), f"Source file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Verify new_secret.key is being referenced
    assert "new_secret.key" in content, f"The file {path} does not reference 'new_secret.key'. Credential rotation logic is missing."

    # Verify open redirect fix logic is present
    has_http_check = "http://" in content or "https://" in content or "http" in content
    assert has_http_check, f"The file {path} does not appear to check for 'http' or 'https' in the redirect URL. Open redirect vulnerability may not be fixed."
    assert "/dashboard" in content, f"The file {path} does not contain the fallback redirect path '/dashboard'."

def test_auth_server_compiled():
    path = "/home/user/auth_service/auth_server"
    assert os.path.isfile(path), f"Compiled binary {path} is missing. The agent did not compile the modified C code."
    assert os.access(path, os.X_OK), f"File {path} is not executable."