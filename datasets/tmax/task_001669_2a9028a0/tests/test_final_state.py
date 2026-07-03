# test_final_state.py

import os
import json
import subprocess
import pytest

CLASSIFIER_SCRIPT = "/home/user/classifier.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
AVAILABLE_RULES = "/home/user/configs/available/network_rules.json"
ENABLED_SYMLINK = "/home/user/configs/enabled/active.json"
SYSTEMD_SERVICE = "/home/user/.config/systemd/user/log-analyzer.service"

def test_classifier_script_exists():
    assert os.path.isfile(CLASSIFIER_SCRIPT), f"Classifier script not found at {CLASSIFIER_SCRIPT}"

def test_adversarial_corpus_clean():
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus dir missing: {CLEAN_CORPUS_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert clean_files, "No clean corpus files found."

    failed_clean = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run(["/usr/bin/python3", CLASSIFIER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(f)

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}"

def test_adversarial_corpus_evil():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus dir missing: {EVIL_CORPUS_DIR}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert evil_files, "No evil corpus files found."

    bypassed_evil = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run(["/usr/bin/python3", CLASSIFIER_SCRIPT, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(f)

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}"

def test_network_rules_json():
    assert os.path.isfile(AVAILABLE_RULES), f"Rules JSON not found at {AVAILABLE_RULES}"
    with open(AVAILABLE_RULES, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {AVAILABLE_RULES} is not valid JSON.")

    # Keys can be case-sensitive depending on extraction, but let's check lowercase mapped or direct
    # The prompt says keys: subnet, restricted_port, quota_mb
    subnet = data.get("subnet")
    restricted_port = data.get("restricted_port")
    quota_mb = data.get("quota_mb")

    assert subnet == "172.16.0.0/12", f"Expected subnet '172.16.0.0/12', got {subnet}"
    assert str(restricted_port) == "8080", f"Expected restricted_port 8080, got {restricted_port}"
    assert float(quota_mb) == 500.0, f"Expected quota_mb 500.0, got {quota_mb}"

def test_enabled_symlink():
    assert os.path.islink(ENABLED_SYMLINK), f"Symlink not found at {ENABLED_SYMLINK}"
    target = os.readlink(ENABLED_SYMLINK)
    assert target == AVAILABLE_RULES, f"Symlink points to {target}, expected {AVAILABLE_RULES}"

def test_systemd_service_file():
    assert os.path.isfile(SYSTEMD_SERVICE), f"Systemd service file not found at {SYSTEMD_SERVICE}"
    with open(SYSTEMD_SERVICE, 'r') as f:
        content = f.read()

    expected_exec_start = "ExecStart=/usr/bin/python3 /home/user/classifier.py /home/user/configs/enabled/active.json"
    assert expected_exec_start in content, f"Expected ExecStart line not found in {SYSTEMD_SERVICE}"

def test_systemd_service_enabled():
    # Run systemctl --user is-enabled log-analyzer.service as 'user'
    # Since pytest runs as the test user (usually root or user), we should just run it.
    # We will set XDG_RUNTIME_DIR to ensure --user works if needed, or just run it.
    env = os.environ.copy()
    if "XDG_RUNTIME_DIR" not in env:
        env["XDG_RUNTIME_DIR"] = f"/run/user/{os.getuid()}"

    result = subprocess.run(
        ["systemctl", "--user", "is-enabled", "log-analyzer.service"],
        capture_output=True, text=True, env=env
    )
    assert result.stdout.strip() == "enabled", f"Service is not enabled. stdout: {result.stdout.strip()}, stderr: {result.stderr.strip()}"