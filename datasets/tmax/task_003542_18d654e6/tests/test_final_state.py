# test_final_state.py

import os
import pytest

def test_v2_directory_and_executable():
    v2_dir = "/home/user/app/v2"
    dispatcher_path = os.path.join(v2_dir, "dispatcher")

    assert os.path.isdir(v2_dir), f"Directory {v2_dir} does not exist."
    assert os.path.isfile(dispatcher_path), f"Dispatcher executable {dispatcher_path} does not exist."
    assert os.access(dispatcher_path, os.X_OK), f"Dispatcher {dispatcher_path} is not executable."

def test_mailing_list_directories():
    announce_dir = "/home/user/mail_queue/lists/announce"
    discuss_dir = "/home/user/mail_queue/lists/discuss"

    assert os.path.isdir(announce_dir), f"Mailing list directory {announce_dir} does not exist."
    assert os.path.isdir(discuss_dir), f"Mailing list directory {discuss_dir} does not exist."

def test_current_symlink_points_to_v2():
    current_symlink = "/home/user/app/current"

    assert os.path.islink(current_symlink), f"{current_symlink} is not a symlink."
    target = os.readlink(current_symlink)
    assert target == "/home/user/app/v2", f"Symlink {current_symlink} points to {target}, expected /home/user/app/v2."

def test_dispatcher_created_symlinks():
    expected_links = {
        "/home/user/mail_queue/lists/announce/abc-123-xyz.eml": "/home/user/mail_queue/incoming/msg1.eml",
        "/home/user/mail_queue/lists/discuss/def-456-uvw.eml": "/home/user/mail_queue/incoming/msg2.eml",
        "/home/user/mail_queue/lists/discuss/789-ghi.eml": "/home/user/mail_queue/incoming/msg3.eml"
    }

    for link_path, expected_target in expected_links.items():
        assert os.path.islink(link_path), f"Expected symlink {link_path} was not created."
        actual_target = os.readlink(link_path)
        assert actual_target == expected_target, f"Symlink {link_path} points to {actual_target}, expected {expected_target}."

def test_process_queue_script():
    script_path = "/home/user/workspace/process_queue.sh"

    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."