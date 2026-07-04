# test_final_state.py

import os
import re
import pytest

BASE_DIR = "/home/user/auth_service"
LOG_FILE = os.path.join(BASE_DIR, "auth.log")
MAKEFILE = os.path.join(BASE_DIR, "Makefile")
MAIN_C = os.path.join(BASE_DIR, "main.c")
NGINX_CONF = os.path.join(BASE_DIR, "nginx.conf")

def test_auth_log_exists_and_correct():
    """Test that auth.log was generated and contains the correct variance and replay detection."""
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} is missing. The server might not have been run or Nginx proxy failed."

    with open(LOG_FILE, "r") as f:
        content = f.read()

    # The variance of "SECRET123" should be around 158.89
    # We look for the expected first request and the replay request.
    expected_first = r"Token:\s*SECRET123,\s*Variance:\s*158\.89,\s*Replay:\s*0"
    expected_replay = r"Token:\s*SECRET123,\s*Variance:\s*158\.89,\s*Replay:\s*1"

    assert re.search(expected_first, content), "The first request for SECRET123 was not logged correctly or variance calculation is wrong."
    assert re.search(expected_replay, content), "The replay request for SECRET123 was not detected correctly."

def test_makefile_fixed():
    """Test that the Makefile was fixed to include ds.o and link the math library."""
    assert os.path.isfile(MAKEFILE), f"Makefile {MAKEFILE} is missing."

    with open(MAKEFILE, "r") as f:
        content = f.read()

    assert "ds.o" in content, "Makefile does not link ds.o."
    assert "-lm" in content, "Makefile does not link the math library (-lm)."

def test_main_c_fixed():
    """Test that the memory safety issue in main.c was fixed."""
    assert os.path.isfile(MAIN_C), f"main.c {MAIN_C} is missing."

    with open(MAIN_C, "r") as f:
        content = f.read()

    # The buffer should be at least 128 characters long
    match = re.search(r"char\s+token\[(\d+)\];", content)
    if match:
        size = int(match.group(1))
        assert size >= 128, f"Buffer size in main.c is {size}, but it should be at least 128 to fix the vulnerability safely."
    else:
        # If they changed the allocation strategy (e.g., malloc), just ensure the old vulnerable buffer is gone
        assert "char token[16];" not in content, "The vulnerable char token[16]; is still present in main.c."

def test_nginx_conf_fixed():
    """Test that Nginx configuration was updated to act as a reverse proxy."""
    assert os.path.isfile(NGINX_CONF), f"nginx.conf {NGINX_CONF} is missing."

    with open(NGINX_CONF, "r") as f:
        content = f.read()

    assert "proxy_pass" in content, "nginx.conf does not contain the 'proxy_pass' directive."
    assert "9000" in content, "nginx.conf does not proxy to the correct port (9000)."