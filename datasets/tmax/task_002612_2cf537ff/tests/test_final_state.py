# test_final_state.py

import os
import stat
import socket
import pytest

def test_backup_file_exists():
    backup_path = "/home/user/backups/deploy_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist. Ensure the deploy script creates it."

def test_git_hook_configured():
    hook_path = "/home/user/repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist. Ensure you created the post-receive hook."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Git hook {hook_path} is not executable. Ensure you set the correct permissions."

def test_success_txt_content():
    success_path = "/home/user/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} does not exist. Did you run the curl command and save its output?"

    with open(success_path, "r") as f:
        content = f.read().strip()

    assert content == "Pipeline Active", f"Expected content 'Pipeline Active' in {success_path}, but found '{content}'."

def test_ports_listening():
    ports_to_check = [8080, 8081]

    for port in ports_to_check:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Port {port} is not listening. Ensure the proxy and backend services are running."