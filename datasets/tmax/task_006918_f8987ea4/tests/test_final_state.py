# test_final_state.py

import os
import stat
import re
import pytest

def test_proxy_bin_exists():
    bin_path = "/home/user/proxy/proxy_bin"
    assert os.path.isfile(bin_path), f"File {bin_path} does not exist. Did you recompile the proxy?"
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_alerts_log_permissions():
    log_path = "/home/user/alerts/alerts.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."
    st = os.stat(log_path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o600, f"Permissions for {log_path} are {oct(mode)}, expected 0o600."

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    # Check for the required directives
    assert "/home/user/alerts/alerts.log" in content, "logrotate.conf does not target /home/user/alerts/alerts.log"
    assert re.search(r'\bdaily\b', content), "logrotate.conf is missing 'daily' directive."
    assert re.search(r'\brotate\s+3\b', content), "logrotate.conf is missing 'rotate 3' directive."
    assert re.search(r'\bmissingok\b', content), "logrotate.conf is missing 'missingok' directive."
    assert re.search(r'\bnotifempty\b', content), "logrotate.conf is missing 'notifempty' directive."

def test_verification_script():
    script_path = "/home/user/test_alert.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    # Check if result.txt was generated and contains 200
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. Did you run the test_alert.sh script?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "200", f"Expected HTTP status code 200 in {result_path}, but got '{content}'."