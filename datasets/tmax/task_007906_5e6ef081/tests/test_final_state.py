# test_final_state.py

import os
import pytest

def test_live_config_symlink():
    symlink_path = "/home/user/config_manager/live_config"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."

    target = os.readlink(symlink_path)
    # The target should be an absolute or relative path that resolves to the versions/a1b2c3d4 directory
    # Let's check if the resolved absolute path contains the expected version directory.
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert "/home/user/config_manager/versions/a1b2c3d4" in abs_target, \
        f"Symlink target {target} does not point to the expected versions/a1b2c3d4 directory."

def test_database_conf_in_live_config():
    db_conf_path = "/home/user/config_manager/live_config/database.conf"
    assert os.path.isfile(db_conf_path), f"Expected configuration file {db_conf_path} does not exist. Did the extraction or symlink fail?"

    with open(db_conf_path, "r") as f:
        content = f.read()

    assert "max_connections=1024" in content, "The database.conf file does not contain the correct max_connections value."

def test_rollback_report():
    report_path = "/home/user/config_manager/rollback_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Rollback Hash: a1b2c3d4\nMax Connections: 1024"
    assert content == expected_content, \
        f"Report file content is incorrect.\nExpected:\n{expected_content}\nGot:\n{content}"