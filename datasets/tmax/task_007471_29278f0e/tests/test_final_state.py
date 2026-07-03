# test_final_state.py

import os
import json

def test_symlink_deleted():
    loop_link = "/home/user/configs/dirA/dirB/loop_link"
    assert not os.path.exists(loop_link) and not os.path.islink(loop_link), \
        f"Symlink loop {loop_link} should have been deleted."

def test_parsed_logs_json():
    json_path = "/home/user/parsed_logs.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    expected_data = [
        {
            "version": 101,
            "author": "Alice Admin",
            "changes": " - Updated firewall rules\n - Opened port 443\n - Closed port 80"
        },
        {
            "version": 102,
            "author": "Bob Backup",
            "changes": " - Configured symlink traversal\n - Added infinite loop detection"
        }
    ]

    assert data == expected_data, f"Parsed JSON data does not match the expected output."

def test_hard_link():
    json_path = "/home/user/parsed_logs.json"
    backup_path = "/home/user/logs_backup.json"

    assert os.path.isfile(backup_path), f"File {backup_path} does not exist."

    stat_json = os.stat(json_path)
    stat_backup = os.stat(backup_path)

    assert stat_json.st_ino == stat_backup.st_ino, \
        f"{backup_path} is not a hard link to {json_path}."

def test_go_parser_exists():
    parser_path = "/home/user/parser.go"
    assert os.path.isfile(parser_path), f"Go program {parser_path} does not exist."