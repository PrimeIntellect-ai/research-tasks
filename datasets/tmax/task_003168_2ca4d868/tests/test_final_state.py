# test_final_state.py
import os
import configparser
import subprocess
import re

def test_environment_hardening():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."

    with open(bashrc_path, "r") as f:
        content = f.read()

    # Allow either export APP_SECURE_MODE=strict or just APP_SECURE_MODE=strict
    assert re.search(r"(?:export\s+)?APP_SECURE_MODE=strict", content), \
        f"APP_SECURE_MODE=strict not found in {bashrc_path}."

def test_app_config_ini():
    config_path = "/home/user/app_config.ini"
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    config = configparser.ConfigParser()
    config.read(config_path)

    assert "security" in config, "Missing [security] section in app_config.ini."
    assert config["security"].get("tls_enabled") == "true", "tls_enabled must be true in [security] section."
    assert config["security"].get("max_connections") == "50", "max_connections must be 50 in [security] section."

    assert "logging" in config, "Missing [logging] section in app_config.ini."
    assert config["logging"].get("path") == "/home/user/app_logs/service.log", \
        "path must be /home/user/app_logs/service.log in [logging] section."

def test_logrotate_conf():
    logrotate_path = "/home/user/logrotate.conf"
    assert os.path.isfile(logrotate_path), f"{logrotate_path} does not exist."

    with open(logrotate_path, "r") as f:
        content = f.read()

    assert "/home/user/app_logs/service.log" in content, "logrotate.conf does not target /home/user/app_logs/service.log."
    assert "daily" in content, "logrotate.conf is missing 'daily' directive."
    assert "rotate 7" in content, "logrotate.conf is missing 'rotate 7' directive."
    assert "compress" in content, "logrotate.conf is missing 'compress' directive."
    assert re.search(r"create\s+(0)?600", content), "logrotate.conf is missing 'create 0600' directive."

def test_health_check_script():
    script_path = "/home/user/monitor.sh"
    log_dir = "/home/user/app_logs"
    log_file = os.path.join(log_dir, "service.log")
    health_file = "/home/user/health.txt"

    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    os.makedirs(log_dir, exist_ok=True)

    # Test 1: Log file does not exist
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(health_file):
        os.remove(health_file)

    subprocess.run([script_path], check=False)
    assert os.path.isfile(health_file), f"{health_file} was not created by the script."
    with open(health_file, "r") as f:
        assert f.read().strip() == "STATUS: UNHEALTHY", "Script did not output STATUS: UNHEALTHY when log file is missing."

    # Test 2: Log file exists but has CRITICAL_ERROR
    with open(log_file, "w") as f:
        f.write("Some info\nCRITICAL_ERROR encountered\n")

    subprocess.run([script_path], check=False)
    with open(health_file, "r") as f:
        assert f.read().strip() == "STATUS: UNHEALTHY", "Script did not output STATUS: UNHEALTHY when log file has CRITICAL_ERROR."

    # Test 3: Log file exists and is healthy
    with open(log_file, "w") as f:
        f.write("Normal startup\nINFO: Running\n")

    subprocess.run([script_path], check=False)
    with open(health_file, "r") as f:
        assert f.read().strip() == "STATUS: HEALTHY", "Script did not output STATUS: HEALTHY when log file is healthy."