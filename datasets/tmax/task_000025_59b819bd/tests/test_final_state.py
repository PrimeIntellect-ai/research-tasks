# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_directories_and_links():
    assert os.path.isdir("/home/user/www/html"), "/home/user/www/html directory is missing."
    assert os.path.isdir("/home/user/nginx/conf"), "/home/user/nginx/conf directory is missing."

    sites_available = "/home/user/nginx/conf/sites-available/app.conf"
    sites_enabled = "/home/user/nginx/conf/sites-enabled/app.conf"

    assert os.path.isfile(sites_available), f"{sites_available} is missing."
    assert os.path.islink(sites_enabled), f"{sites_enabled} is not a symlink."

    target = os.readlink(sites_enabled)
    # Could be absolute or relative, resolve it
    resolved_target = os.path.normpath(os.path.join(os.path.dirname(sites_enabled), target))
    assert resolved_target == sites_available, f"Symlink {sites_enabled} does not point to {sites_available}."

def test_backup_and_config():
    backup_file = "/home/user/backup/nginx.conf.bak"
    assert os.path.isfile(backup_file), f"Backup file {backup_file} is missing."

    with open(backup_file, "r") as f:
        backup_content = f.read()
    assert "proxy_pass http://127.0.0.1:8080;" in backup_content, "Backup file does not match original content."

    app_conf = "/home/user/nginx/conf/sites-available/app.conf"
    with open(app_conf, "r") as f:
        app_content = f.read()
    assert "proxy_pass http://127.0.0.1:9090;" in app_content, "app.conf does not contain the updated port 9090."
    assert "8080" not in app_content, "app.conf still contains the old port 8080."

def test_fake_fstab():
    fstab_file = "/home/user/fake_fstab"
    assert os.path.isfile(fstab_file), f"{fstab_file} is missing."

    with open(fstab_file, "r") as f:
        content = f.read()

    # Check for the required mount entry components
    assert "/home/user/data.img" in content
    assert "/home/user/www/html/data" in content
    assert "ext4" in content
    assert "defaults" in content

def test_expect_script():
    expect_script = "/home/user/test_backend.exp"
    assert os.path.isfile(expect_script), f"{expect_script} is missing."

    with open(expect_script, "r") as f:
        content = f.read()

    assert "spawn" in content, "Expect script missing 'spawn' command."
    assert "PING" in content, "Expect script missing 'PING' string."
    assert "PONG" in content, "Expect script missing 'PONG' string."

def test_fuzz_equivalence():
    oracle = "/app/legacy_auth"
    agent = "/home/user/new_backend.py"

    assert os.path.isfile(oracle), f"Oracle {oracle} is missing."
    assert os.path.isfile(agent), f"Agent script {agent} is missing."

    random.seed(42)
    chars = string.ascii_letters + string.digits

    for _ in range(500):
        length = random.randint(8, 64)
        fuzz_input = "".join(random.choice(chars) for _ in range(length))

        oracle_res = subprocess.run([oracle, fuzz_input], capture_output=True, text=True)
        agent_res = subprocess.run(["python3", agent, fuzz_input], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed with return code {agent_res.returncode} on input '{fuzz_input}'\nStderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout
        agent_out = agent_res.stdout

        assert oracle_out == agent_out, f"Mismatch on input '{fuzz_input}'.\nOracle output: {repr(oracle_out)}\nAgent output: {repr(agent_out)}"