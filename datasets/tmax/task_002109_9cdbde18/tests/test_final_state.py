# test_final_state.py

import os
import subprocess
import yaml
import pytest

def test_docker_compose_network_fix():
    compose_path = "/home/user/capacity-stack/docker-compose.yml"
    assert os.path.isfile(compose_path), f"Missing {compose_path}"

    with open(compose_path, 'r') as f:
        compose_data = yaml.safe_load(f)

    services = compose_data.get('services', {})
    assert 'log_aggregator' in services, "log_aggregator service missing"
    assert 'db' in services, "db service missing"

    log_aggregator_nets = services['log_aggregator'].get('networks', [])
    db_nets = services['db'].get('networks', [])

    assert 'capacity_net' in log_aggregator_nets, "log_aggregator is not on capacity_net"
    assert 'capacity_net' in db_nets, "db is not on capacity_net"

def test_automate_interactive_backup():
    script_path = "/home/user/run_backup.py"
    target_archive = "/home/user/backups/latest.tar.gz"

    assert os.path.isfile(script_path), f"Missing backup script: {script_path}"

    # Remove the target archive if it exists from a previous run
    if os.path.exists(target_archive):
        os.remove(target_archive)

    # Run the student's script
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_backup.py failed with exit code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile(target_archive), f"Backup archive not found at {target_archive} after running script."

def test_adversarial_log_sanitizer():
    sanitizer_path = "/home/user/sanitize.py"
    assert os.path.isfile(sanitizer_path), f"Missing sanitizer script: {sanitizer_path}"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    failed_clean = []
    for cf in clean_files:
        result = subprocess.run(["python3", sanitizer_path, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        result = subprocess.run(["python3", sanitizer_path, ef], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_msg = []
    if failed_evil:
        error_msg.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_msg.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")

    assert not error_msg, "Sanitizer failed criteria:\n" + "\n".join(error_msg)