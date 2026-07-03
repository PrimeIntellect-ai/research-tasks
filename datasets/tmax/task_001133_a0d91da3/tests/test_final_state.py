# test_final_state.py
import os

def test_backup_and_directories():
    backup_file = "/home/user/backup/nginx.conf.bak"
    logs_dir = "/home/user/app/logs"

    assert os.path.isfile(backup_file), f"Backup file {backup_file} is missing."
    assert os.path.isdir(logs_dir), f"Logs directory {logs_dir} is missing."

def test_symlink():
    symlink_path = "/home/user/active_conf"
    target_path = "/home/user/app/conf/nginx.conf"

    assert os.path.islink(symlink_path), f"Symlink {symlink_path} is missing or is not a symlink."
    target = os.readlink(symlink_path)
    assert target == target_path, f"Symlink points to {target} instead of {target_path}."

def test_nginx_config_updated():
    conf_path = "/home/user/app/conf/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:9999" not in content, "Nginx config still points to the broken port 9999."
    assert "127.0.0.1:8081" in content, "Nginx config does not point to the correct backend port 8081."

def test_backend_compiled():
    backend_path = "/home/user/app/backend"
    assert os.path.isfile(backend_path), f"Compiled backend {backend_path} is missing."
    assert os.access(backend_path, os.X_OK), f"Compiled backend {backend_path} is not executable."

def test_resolution_log():
    log_path = "/home/user/resolution.log"
    assert os.path.isfile(log_path), f"Resolution log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "OK" in content, f"Resolution log does not contain 'OK'. Actual content: {content.strip()}"