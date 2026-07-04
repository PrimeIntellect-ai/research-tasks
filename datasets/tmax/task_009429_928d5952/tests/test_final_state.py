# test_final_state.py

import os
import pytest

def test_script_exists_and_uses_flock():
    script_path = "/home/user/organizer.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, f"Script {script_path} does not seem to use fcntl.flock as required."

def test_project_logs_directory_empty():
    source_dir = "/home/user/project_logs"
    assert os.path.isdir(source_dir), f"Source directory {source_dir} is missing."

    files = os.listdir(source_dir)
    assert len(files) == 0, f"Source directory {source_dir} is not empty. Contains: {files}"

def test_organized_logs_exist_and_correct():
    target_dir = "/home/user/organized_logs"
    assert os.path.isdir(target_dir), f"Target directory {target_dir} is missing."

    expected_files = {
        "security_logs/warning_x99_auth.log": "x99_auth",
        "backend_logs/critical_db_88_conn.log": "db_88_conn",
        "frontend_logs/info_ui_77_render.log": "ui_77_render"
    }

    for rel_path, id_str in expected_files.items():
        full_path = os.path.join(target_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected organized log file {full_path} is missing."

        with open(full_path, "r") as f:
            content = f.read()

        assert "<<<JSON_START>>>" in content, f"Log content missing JSON_START in {full_path}"
        assert id_str in content, f"Expected ID '{id_str}' not found in {full_path}"