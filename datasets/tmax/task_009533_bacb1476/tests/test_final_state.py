# test_final_state.py

import os
import re
import stat

def test_nginx_config_updated():
    nginx_conf_path = "/home/user/microservices-config/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File {nginx_conf_path} does not exist."

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # We check that the new ports are present and the old ports are gone.
    assert "127.0.0.1:8081" in content, "nginx.conf does not route to 127.0.0.1:8081 for /auth."
    assert "127.0.0.1:8082" in content, "nginx.conf does not route to 127.0.0.1:8082 for /data."
    assert "127.0.0.1:9000" not in content, "nginx.conf still contains the old port 9000."
    assert "127.0.0.1:9001" not in content, "nginx.conf still contains the old port 9001."

def test_bashrc_env_vars():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"File {bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    # Check for AUTH_SECRET
    auth_secret_match = re.search(r'AUTH_SECRET\s*=\s*["\']?supersecret["\']?', content)
    assert auth_secret_match is not None, "AUTH_SECRET is not correctly set to 'supersecret' in .bashrc."

    # Check for DATA_DIR
    data_dir_match = re.search(r'DATA_DIR\s*=\s*["\']?/home/user/data["\']?', content)
    assert data_dir_match is not None, "DATA_DIR is not correctly set to '/home/user/data' in .bashrc."

def test_git_pre_commit_hook():
    hook_path = "/home/user/microservices-config/.git/hooks/pre-commit"
    assert os.path.isfile(hook_path), f"Pre-commit hook file {hook_path} does not exist."

    # Check if executable
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pre-commit hook {hook_path} is not executable."

    with open(hook_path, "r") as f:
        content = f.read()

    assert "validate.sh" in content, "Pre-commit hook does not appear to call validate.sh."

def test_cron_schedule():
    cron_file_path = "/home/user/cron_schedule.txt"
    assert os.path.isfile(cron_file_path), f"File {cron_file_path} does not exist."

    with open(cron_file_path, "r") as f:
        content = f.read().strip()

    # Remove extra spaces/tabs between fields to normalize
    normalized_content = re.sub(r'\s+', ' ', content)
    expected_schedule = "0 2 * * * /home/user/backup.sh"

    assert normalized_content == expected_schedule, f"Cron schedule is incorrect. Expected '{expected_schedule}', got '{normalized_content}'."