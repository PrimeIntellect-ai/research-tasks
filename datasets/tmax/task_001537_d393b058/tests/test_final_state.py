# test_final_state.py
import os
import re
import subprocess
import random
import string
import tempfile
import shutil
import pytest

ORACLE_PATH = "/app/legacy_ticket_extractor"
AGENT_PATH = "/home/user/ticket_extractor"
REPO_PATH = "/home/user/config_repo.git"
LOG_PATH = "/home/user/repo_activity.log"
LOGROTATE_CONF = "/home/user/repo_logrotate.conf"
CHECK_STORAGE_SCRIPT = "/home/user/check_storage.sh"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " \n\t\r"

    for i in range(5000):
        length = random.randint(0, 1024)
        input_data = "".join(random.choices(charset, k=length)).encode('utf-8')

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on input {input_data!r}"
        assert oracle_proc.stdout == agent_proc.stdout, f"Stdout mismatch on input {input_data!r}. Expected {oracle_proc.stdout!r}, got {agent_proc.stdout!r}"
        assert oracle_proc.stderr == agent_proc.stderr, f"Stderr mismatch on input {input_data!r}. Expected {oracle_proc.stderr!r}, got {agent_proc.stderr!r}"

def test_git_hook_functionality():
    assert os.path.exists(REPO_PATH), f"Git repo missing at {REPO_PATH}"

    # Create a temporary clone to push from
    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "clone")
        subprocess.run(["git", "clone", REPO_PATH, clone_dir], check=True, capture_output=True)

        # Make a commit
        test_file = os.path.join(clone_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        subprocess.run(["git", "add", "test.txt"], cwd=clone_dir, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "Fixes VANGUARD-8821 and also bugs"], cwd=clone_dir, check=True, capture_output=True)

        # Push to trigger hook
        subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, check=True, capture_output=True)

    assert os.path.exists(LOG_PATH), f"Log file missing at {LOG_PATH}"

    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Codename VANGUARD-8821 processed"
    assert re.search(pattern, log_content), f"Expected log entry not found in {LOG_PATH}"

def test_logrotate_conf():
    assert os.path.exists(LOGROTATE_CONF), f"Logrotate conf missing at {LOGROTATE_CONF}"

    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    assert "daily" in content, "Missing 'daily' directive in logrotate conf"
    assert "rotate 7" in content, "Missing 'rotate 7' directive in logrotate conf"
    assert "compress" in content, "Missing 'compress' directive in logrotate conf"
    assert LOG_PATH in content, f"Logrotate conf does not target {LOG_PATH}"

def test_crontab():
    proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert proc.returncode == 0, "Failed to read crontab"

    crontab_content = proc.stdout

    assert re.search(r"0\s+\*\s+\*\s+\*\s+\*\s+/home/user/check_storage\.sh", crontab_content), "Missing check_storage.sh crontab entry"
    assert re.search(r"0\s+0\s+\*\s+\*\s+\*\s+logrotate\s+/home/user/repo_logrotate\.conf\s+--state\s+/home/user/logrotate\.state", crontab_content), "Missing logrotate crontab entry"

def test_check_storage_script():
    assert os.path.exists(CHECK_STORAGE_SCRIPT), f"Storage check script missing at {CHECK_STORAGE_SCRIPT}"
    assert os.access(CHECK_STORAGE_SCRIPT, os.X_OK), f"Storage check script at {CHECK_STORAGE_SCRIPT} is not executable"

    # Dump a 60MB file into the bare repo
    dummy_file = os.path.join(REPO_PATH, "dummy_60mb.bin")
    try:
        with open(dummy_file, "wb") as f:
            f.write(os.urandom(60 * 1024 * 1024))

        subprocess.run([CHECK_STORAGE_SCRIPT], check=True, capture_output=True)

        assert os.path.exists(LOG_PATH), f"Log file missing at {LOG_PATH}"
        with open(LOG_PATH, "r") as f:
            log_content = f.read()

        assert "WARNING: QUOTA EXCEEDED" in log_content, "Storage check script failed to append warning to log"
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)