# test_final_state.py

import os
import pytest

def test_migration_status_log():
    log_path = "/home/user/migration_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "MIGRATION_COMPLETE", f"Log file {log_path} does not contain exactly 'MIGRATION_COMPLETE'."

def test_exported_data_exists():
    app1_config = "/home/user/export_data/app1/config.txt"
    db_schema = "/home/user/export_data/db_data/schema.sql"

    assert os.path.isfile(app1_config), f"Exported file {app1_config} does not exist."
    assert os.path.isfile(db_schema), f"Exported file {db_schema} does not exist."

def test_symlinks_created():
    app1_link = "/home/user/cloud_mounts/srv/app1"
    db_link = "/home/user/cloud_mounts/var/lib/db"

    # Check app1 link
    assert os.path.islink(app1_link), f"{app1_link} is not a symbolic link."
    assert os.readlink(app1_link) == "/home/user/export_data/app1", f"Symlink {app1_link} points to the wrong target."

    # Check db_data link
    assert os.path.islink(db_link), f"{db_link} is not a symbolic link."
    assert os.readlink(db_link) == "/home/user/export_data/db_data", f"Symlink {db_link} points to the wrong target."

def test_scripts_exist():
    run_export_script = "/home/user/run_export.py"
    setup_mounts_script = "/home/user/setup_mounts.py"

    assert os.path.isfile(run_export_script), f"Script {run_export_script} was not created."
    assert os.path.isfile(setup_mounts_script), f"Script {setup_mounts_script} was not created."