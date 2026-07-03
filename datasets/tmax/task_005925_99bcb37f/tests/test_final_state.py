# test_final_state.py

import os
import pytest

def test_scripts_exist():
    """Verify that the required scripts were created."""
    assert os.path.exists('/home/user/backend_v2.py'), "backend_v2.py is missing."
    assert os.path.exists('/home/user/proxy.py'), "proxy.py is missing."

def test_results_log_exists():
    """Verify that the results log file was created."""
    assert os.path.exists('/home/user/results.log'), "results.log does not exist."

def test_results_log_content():
    """Verify the exact responses from the curl commands in the results log."""
    with open('/home/user/results.log', 'r') as f:
        content = f.read()

    # Normalize newlines to handle both concatenated and newline-separated outputs
    normalized_content = content.replace('\n', '').replace('\r', '')
    expected_content = "V1 Legacy APIV1 Legacy APIollehWORLDV1 Legacy API"

    assert normalized_content == expected_content, (
        f"Log file contents do not match expected responses.\n"
        f"Expected (normalized): {expected_content}\n"
        f"Actual (normalized): {normalized_content}\n"
        f"Raw content: {repr(content)}"
    )