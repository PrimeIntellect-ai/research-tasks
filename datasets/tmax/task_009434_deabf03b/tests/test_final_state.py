# test_final_state.py

import os
import pytest

API_SERVER_DIR = "/home/user/api_server"
LOG_FILE = os.path.join(API_SERVER_DIR, "status_codes.log")
MAKEFILE = os.path.join(API_SERVER_DIR, "Makefile")
SERVER_EXEC = os.path.join(API_SERVER_DIR, "server")

def test_status_codes_log_exists():
    assert os.path.isfile(LOG_FILE), f"The log file {LOG_FILE} was not found."

def test_status_codes_log_content():
    with open(LOG_FILE, "r") as f:
        content = f.read().strip()

    expected_content = "200,200,200,429,429,429,429,429"
    assert content == expected_content, (
        f"The contents of {LOG_FILE} did not match the expected status codes.\n"
        f"Expected: {expected_content}\n"
        f"Got:      {content}"
    )

def test_server_executable_exists():
    assert os.path.isfile(SERVER_EXEC), (
        f"The server executable {SERVER_EXEC} does not exist. "
        "Did you successfully run 'make'?"
    )
    assert os.access(SERVER_EXEC, os.X_OK), f"The file {SERVER_EXEC} is not executable."

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE), f"The Makefile {MAKEFILE} was not found."
    with open(MAKEFILE, "r") as f:
        content = f.read()

    # The linking step needs both math and pthread libraries.
    # Acceptable flags for pthread include -lpthread or -pthread.
    has_math = "-lm" in content
    has_pthread = "-lpthread" in content or "-pthread" in content

    assert has_math, "The Makefile does not contain the '-lm' flag required for math library linking."
    assert has_pthread, "The Makefile does not contain the '-lpthread' or '-pthread' flag required for threading."