# test_final_state.py

import os
import re
import pytest

def test_port_forward_service_exists_and_correct():
    path = "/home/user/.config/systemd/user/port-forward.service"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "Restart=always" in content, f"File {path} is missing 'Restart=always'."

    # Check for socat command listening on 10025 and forwarding to 127.0.0.1:2525
    assert "socat" in content, f"File {path} does not seem to run socat."
    assert "10025" in content, f"File {path} does not configure port 10025."
    assert "2525" in content, f"File {path} does not configure forwarding to port 2525."

def test_mailer_app_cpp_fixed():
    path = "/home/user/mailer_app.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "htons(10025)" in content, f"File {path} does not contain the fixed port htons(10025)."
    assert "htons(10024)" not in content, f"File {path} still contains the buggy port htons(10024)."

def test_mailer_app_compiled():
    path = "/home/user/mailer_app"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_mailer_app_service_dependencies():
    path = "/home/user/.config/systemd/user/mailer_app.service"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert re.search(r"^Requires=.*port-forward\.service", content, re.MULTILINE), f"File {path} is missing Requires=port-forward.service."
    assert re.search(r"^After=.*port-forward\.service", content, re.MULTILINE), f"File {path} is missing After=port-forward.service."

def test_mail_spool_log_contains_status_fixed():
    path = "/home/user/mail_spool.log"
    assert os.path.isfile(path), f"File {path} does not exist. The application may not have run successfully."
    with open(path, "r") as f:
        content = f.read()
    assert "STATUS: FIXED" in content, f"File {path} does not contain 'STATUS: FIXED'. The mailer app did not successfully deliver the message."