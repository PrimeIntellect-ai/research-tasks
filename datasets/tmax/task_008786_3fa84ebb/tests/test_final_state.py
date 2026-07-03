# test_final_state.py

import os
import json
import stat
import pytest

def test_users_json_exists_and_valid():
    users_file = "/home/user/backup_op/users.json"
    assert os.path.isfile(users_file), f"File {users_file} does not exist."

    with open(users_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {users_file} does not contain valid JSON.")

    assert "users" in data, f"'users' key missing in {users_file}"
    assert len(data["users"]) > 0, f"'users' list is empty in {users_file}"

    user_obj = data["users"][0]
    assert user_obj.get("username") == "backup_agent", "Username should be 'backup_agent'."
    assert user_obj.get("group") == "system_admins", "Group should be 'system_admins'."
    assert user_obj.get("token") == "pipeline-token-883", "Token should be 'pipeline-token-883'."

def test_restore_client_ip_fixed():
    main_rs = "/home/user/backup_op/restore_client/src/main.rs"
    assert os.path.isfile(main_rs), f"File {main_rs} does not exist."

    with open(main_rs, 'r') as f:
        content = f.read()

    assert "127.0.0.2:9090" in content, f"The IP address in {main_rs} was not updated to 127.0.0.2:9090."
    assert "127.0.0.1:9090" not in content, f"The old IP address 127.0.0.1:9090 is still present in {main_rs}."

def test_run_pipeline_script_executable():
    script_path = "/home/user/backup_op/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_restore_success_log():
    log_file = "/home/user/backup_op/restore_success.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist. Did you run the pipeline script?"

    with open(log_file, 'r') as f:
        content = f.read()

    assert "BACKUP_DATA_RESTORED_V1" in content, f"The expected success payload 'BACKUP_DATA_RESTORED_V1' was not found in {log_file}."