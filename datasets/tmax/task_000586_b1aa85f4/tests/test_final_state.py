# test_final_state.py
import json
import os
import pytest

def test_deps_appserver_json():
    path = '/home/user/deps_AppServer.json'
    assert os.path.exists(path), f"{path} is missing. The script did not generate the output for AppServer."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert 'server' in data, f"'server' key missing in {path}"
    assert data['server'] == 'AppServer', f"Expected server 'AppServer', got {data['server']}"

    assert 'dependsOn' in data, f"'dependsOn' key missing in {path}"
    assert isinstance(data['dependsOn'], list), f"'dependsOn' should be a list in {path}"

    expected_deps = ['DB_Primary', 'Redis_Cache']
    actual_deps = data['dependsOn']
    assert sorted(actual_deps) == expected_deps, f"Expected dependencies {expected_deps}, got {actual_deps}"
    assert actual_deps == sorted(actual_deps), f"Dependencies in {path} must be sorted alphabetically."

def test_deps_db_primary_json():
    path = '/home/user/deps_DB_Primary.json'
    assert os.path.exists(path), f"{path} is missing. The script did not generate the output for DB_Primary."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert 'server' in data, f"'server' key missing in {path}"
    assert data['server'] == 'DB_Primary', f"Expected server 'DB_Primary', got {data['server']}"

    assert 'dependsOn' in data, f"'dependsOn' key missing in {path}"
    assert isinstance(data['dependsOn'], list), f"'dependsOn' should be a list in {path}"

    expected_deps = ['AuthService', 'Storage_SAN']
    actual_deps = data['dependsOn']
    assert sorted(actual_deps) == expected_deps, f"Expected dependencies {expected_deps}, got {actual_deps}"
    assert actual_deps == sorted(actual_deps), f"Dependencies in {path} must be sorted alphabetically."

def test_query_index_csv():
    path = '/home/user/query_index.csv'
    assert os.path.exists(path), f"{path} is missing. The index file was not created."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_appserver = "AppServer,DB_Primary|Redis_Cache"
    expected_db_primary = "DB_Primary,AuthService|Storage_SAN"

    assert expected_appserver in lines, f"Expected '{expected_appserver}' in {path}"
    assert expected_db_primary in lines, f"Expected '{expected_db_primary}' in {path}"

def test_check_deps_script_exists():
    path = '/home/user/check_deps.sh'
    assert os.path.exists(path), f"{path} is missing. The bash script was not created."
    assert os.path.isfile(path), f"{path} is not a file."