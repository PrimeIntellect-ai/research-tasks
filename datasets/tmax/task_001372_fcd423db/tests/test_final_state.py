# test_final_state.py

import os
import pytest

def test_live_app1_content():
    path = "/home/user/live/app1.conf"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "DEPLOY=true" in content, f"{path} is missing DEPLOY=true"
    assert "SETTING1=foo" in content, f"{path} is missing SETTING1=foo"
    assert "SETTING2=bar" in content, f"{path} is missing SETTING2=bar"

def test_live_app3_content():
    path = "/home/user/live/app3.conf"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "DEPLOY=true" in content, f"{path} is missing DEPLOY=true"
    assert "SETTING1=baz" in content, f"{path} is missing SETTING1=baz"

def test_live_app2_missing():
    path = "/home/user/live/app2.conf"
    assert not os.path.exists(path), f"{path} should not exist because DEPLOY was not true."

def test_backup_app1_content():
    path = "/home/user/backup/app1.conf.bak"
    assert os.path.isfile(path), f"Backup file {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "SETTING1=old_foo" in content, f"Backup file {path} does not contain the old content."

def test_deploy_log():
    path = "/home/user/deploy.log"
    assert os.path.isfile(path), f"Log file {path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "Successfully deployed app1.conf" in lines, f"Log missing success message for app1.conf"
    assert "Successfully deployed app3.conf" in lines, f"Log missing success message for app3.conf"
    assert "Successfully deployed app2.conf" not in lines, f"Log incorrectly contains success message for app2.conf"

def test_no_tmp_files():
    live_dir = "/home/user/live"
    assert os.path.isdir(live_dir), f"Directory {live_dir} is missing."
    for filename in os.listdir(live_dir):
        assert not (filename.startswith(".") and filename.endswith(".tmp")), f"Temporary file {filename} was left in {live_dir}."