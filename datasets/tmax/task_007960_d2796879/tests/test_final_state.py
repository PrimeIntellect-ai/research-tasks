# test_final_state.py

import os
import re
import pytest

def test_cleaner_executable():
    """Check if /home/user/cleaner exists and is executable."""
    path = '/home/user/cleaner'
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_process_sh_executable():
    """Check if /home/user/process.sh exists and is executable."""
    path = '/home/user/process.sh'
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_clean_configs_server1():
    """Check contents of /home/user/clean_configs/server1.conf."""
    path = '/home/user/clean_configs/server1.conf'
    assert os.path.isfile(path), f"Cleaned config {path} does not exist."

    expected_content = "host = 192.168.1.10\nport=8080\ntimeout = 30\n"
    with open(path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {path} is incorrect."

def test_clean_configs_server2():
    """Check contents of /home/user/clean_configs/server2.conf."""
    path = '/home/user/clean_configs/server2.conf'
    assert os.path.isfile(path), f"Cleaned config {path} does not exist."

    expected_content = "loglevel=debug\npath=/var/log/app.log\n"
    with open(path, 'r') as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {path} is incorrect."

def test_cron_txt():
    """Check if /home/user/cron.txt contains the correct cron job."""
    path = '/home/user/cron.txt'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    pattern = r'^(\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*\s+/home/user/process\.sh$'
    assert re.match(pattern, content), f"Content of {path} does not match the expected crontab format."