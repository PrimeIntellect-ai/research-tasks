# test_final_state.py

import os
import json
import pytest

def test_project_directory_exists():
    assert os.path.isdir('/home/user/project'), "Directory /home/user/project does not exist."

def test_files_renamed_no_dev_prefix():
    project_files = os.listdir('/home/user/project')
    for f in project_files:
        assert not f.startswith('dev_'), f"File {f} still has the 'dev_' prefix."

def test_csv_to_json_conversion():
    settings_json_path = '/home/user/project/settings.json'
    data_json_path = '/home/user/project/data.json'

    assert os.path.isfile(settings_json_path), f"JSON file {settings_json_path} does not exist."
    assert os.path.isfile(data_json_path), f"JSON file {data_json_path} does not exist."

    with open(settings_json_path, 'r') as f:
        settings_data = json.load(f)

    expected_settings = [{"key": "theme", "value": "dark"}, {"key": "port", "value": "8080"}]
    assert settings_data == expected_settings, f"Contents of {settings_json_path} are incorrect."

    with open(data_json_path, 'r') as f:
        data_data = json.load(f)

    expected_data = [{"id": "1", "user": "admin"}, {"id": "2", "user": "guest"}]
    assert data_data == expected_data, f"Contents of {data_json_path} are incorrect."

def test_csv_files_deleted():
    assert not os.path.exists('/home/user/project/settings.csv'), "settings.csv was not deleted."
    assert not os.path.exists('/home/user/project/data.csv'), "data.csv was not deleted."
    assert not os.path.exists('/home/user/project/dev_settings.csv'), "dev_settings.csv was not deleted."
    assert not os.path.exists('/home/user/project/dev_data.csv'), "dev_data.csv was not deleted."

def test_critical_errors_extracted():
    errors_path = '/home/user/project/critical_errors.txt'
    assert os.path.isfile(errors_path), f"File {errors_path} does not exist."

    with open(errors_path, 'r') as f:
        lines = f.read().splitlines()

    expected_lines = [
        "CRITICAL: Database connection lost",
        "CRITICAL: Disk full"
    ]

    assert lines == expected_lines, "critical_errors.txt does not contain the correct CRITICAL lines."

def test_symlinks_created():
    assets_dir = '/home/user/public_html/assets'
    assert os.path.isdir(assets_dir), f"Directory {assets_dir} does not exist."

    bg_link = os.path.join(assets_dir, 'background.png')
    icon_link = os.path.join(assets_dir, 'icon.png')

    assert os.path.islink(bg_link), f"{bg_link} is not a symlink."
    assert os.readlink(bg_link) == '/home/user/project/background.png', f"{bg_link} does not point to the correct absolute path."

    assert os.path.islink(icon_link), f"{icon_link} is not a symlink."
    assert os.readlink(icon_link) == '/home/user/project/icon.png', f"{icon_link} does not point to the correct absolute path."