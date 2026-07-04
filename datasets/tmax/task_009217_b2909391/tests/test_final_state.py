# test_final_state.py

import os
import subprocess
import pytest

def test_executables_built():
    assert os.path.isfile("/home/user/app/server"), "The server executable was not built."
    assert os.path.isfile("/home/user/app/client"), "The client executable was not built."

    # Check if they are executable
    assert os.access("/home/user/app/server", os.X_OK), "The server file is not executable."
    assert os.access("/home/user/app/client", os.X_OK), "The client file is not executable."

def test_test_results_log_exists():
    assert os.path.isfile("/home/user/test_results.log"), "The /home/user/test_results.log file is missing."

def test_test_results_log_content():
    expected_content = [
        "Req 1: OK",
        "Req 2: OK",
        "Req 3: OK",
        "Req 4: RATE_LIMITED",
        "Req 5: RATE_LIMITED"
    ]

    with open("/home/user/test_results.log", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines in test_results.log, but found {len(lines)}."

    for i, expected in enumerate(expected_content):
        assert lines[i] == expected, f"Line {i+1} in test_results.log is incorrect. Expected '{expected}', got '{lines[i]}'."

def test_server_rpath_configured():
    # Verify that the server executable has the rpath configured correctly
    # We can do this by using ldd or readelf
    try:
        output = subprocess.check_output(["readelf", "-d", "/home/user/app/server"], stderr=subprocess.STDOUT, text=True)
        assert "RUNPATH" in output or "RPATH" in output, "The server executable does not have RPATH/RUNPATH configured."
        assert "/home/user/app" in output, "The server executable RPATH/RUNPATH does not point to /home/user/app."
    except FileNotFoundError:
        # Fallback if readelf is not available
        pass