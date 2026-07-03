# test_final_state.py

import os
import json
import stat

def test_auto_migrate_script_exists_and_executable():
    script_path = '/home/user/auto_migrate.py'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

    # Check if the script is executable
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"The script {script_path} is not executable by the user."

def test_migration_log_contains_expected_state():
    log_file = '/home/user/migration_log.json'
    assert os.path.exists(log_file), f"The migration log file {log_file} does not exist. Did the script run successfully?"
    assert os.path.isfile(log_file), f"The path {log_file} is not a file."

    with open(log_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {log_file} does not contain valid JSON."

    expected_services = ['worker-1', 'worker-2', 'worker-3']

    for srv in expected_services:
        assert srv in data, f"Missing '{srv}' in {log_file}."

        srv_data = data[srv]
        assert 'version' in srv_data, f"Missing 'version' for '{srv}' in {log_file}."
        assert srv_data['version'] == 'v2.1', f"Expected version 'v2.1' for '{srv}', but got '{srv_data['version']}'."

        assert 'status' in srv_data, f"Missing 'status' for '{srv}' in {log_file}."
        assert srv_data['status'] == 'online', f"Expected status 'online' for '{srv}', but got '{srv_data['status']}'."