# test_final_state.py

import os

def test_success_log_exists_and_passes():
    log_path = "/home/user/math_service/success.log"

    assert os.path.exists(log_path), (
        f"The success log was not found at {log_path}. "
        "Ensure you have run `python3 test_service.py` after fixing all issues."
    )

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "PASS" in content, (
        f"The success log at {log_path} does not contain 'PASS'. "
        "The tests in test_service.py might have failed or not completed successfully."
    )