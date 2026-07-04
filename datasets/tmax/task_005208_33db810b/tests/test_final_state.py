# test_final_state.py

import os
import stat
import tarfile
import urllib.request
import urllib.error

def test_phase1_backup_exists_and_valid():
    backup_path = "/home/user/backups/legacy_data.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if the config.ini is in the tar
            # It might be stored as legacy_data/config.ini or /home/user/legacy_data/config.ini
            assert any("config.ini" in name for name in names), "config.ini not found in the backup archive."
    except tarfile.TarError:
        pytest.fail(f"File {backup_path} is not a valid gzip-compressed tar archive.")

def test_phase2_service_manager_script():
    script_path = "/home/user/service_manager.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_phase2_service_running():
    pid_file = "/home/user/app.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist. Did you start the service?"

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

    pid = int(pid_str)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")

def test_phase2_service_listening():
    try:
        req = urllib.request.Request("http://localhost:8080")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, "Service is not returning HTTP 200."
    except urllib.error.URLError as e:
        pytest.fail(f"Service is not listening on port 8080 or failed to respond: {e}")

def test_phase3_create_admins_script():
    script_path = "/home/user/create_admins.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "useradd -m -G admin admin" in content, "Missing useradd command for 'admin'."
    assert "useradd -m -G admin msmith" in content, "Missing useradd command for 'msmith'."
    assert "jdoe" not in content, "Script should not contain useradd command for non-admin 'jdoe'."

def test_phase3_firewall_rules():
    rules_path = "/home/user/firewall.rules"
    assert os.path.isfile(rules_path), f"Firewall rules file {rules_path} does not exist."

    with open(rules_path, "r") as f:
        content = f.read()

    expected_rule1 = "iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080"
    expected_rule2 = "iptables -A INPUT -p tcp --dport 8080 -j ACCEPT"

    assert expected_rule1 in content, f"Missing expected iptables PREROUTING rule in {rules_path}."
    assert expected_rule2 in content, f"Missing expected iptables INPUT rule in {rules_path}."