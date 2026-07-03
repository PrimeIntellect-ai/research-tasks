# test_final_state.py

import os
import subprocess
import pytest

def test_ssh_monitor_exists_and_executable():
    script_path = "/home/user/ssh_monitor.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_supervisord_conf():
    conf_path = "/home/user/supervisord.conf"
    assert os.path.isfile(conf_path), f"Config {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "[program:ssh_monitor_daemon]" in content, f"Config {conf_path} missing [program:ssh_monitor_daemon] section."

def test_clean_corpus():
    script_path = "/home/user/ssh_monitor.py"
    clean_dir = "/app/corpora/clean"

    result = subprocess.run(["python3", script_path, clean_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on clean corpus. Stderr: {result.stderr}"

    output = result.stdout.strip().splitlines()

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".log")]

    evil_flagged = []
    clean_flagged = []

    for line in output:
        if line.startswith("EVIL:"):
            evil_flagged.append(line.split(":", 1)[1].strip())
        elif line.startswith("CLEAN:"):
            clean_flagged.append(line.split(":", 1)[1].strip())

    assert len(evil_flagged) == 0, f"{len(evil_flagged)} of {len(clean_files)} clean logs flagged as EVIL: {', '.join(evil_flagged)}"

    for f in clean_files:
        assert f in clean_flagged, f"Clean log {f} was not flagged as CLEAN."

def test_evil_corpus():
    script_path = "/home/user/ssh_monitor.py"
    evil_dir = "/app/corpora/evil"

    result = subprocess.run(["python3", script_path, evil_dir], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on evil corpus. Stderr: {result.stderr}"

    output = result.stdout.strip().splitlines()

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".log")]

    evil_flagged = []
    clean_flagged = []

    for line in output:
        if line.startswith("EVIL:"):
            evil_flagged.append(line.split(":", 1)[1].strip())
        elif line.startswith("CLEAN:"):
            clean_flagged.append(line.split(":", 1)[1].strip())

    assert len(clean_flagged) == 0, f"{len(clean_flagged)} of {len(evil_files)} evil logs flagged as CLEAN: {', '.join(clean_flagged)}"

    for f in evil_files:
        assert f in evil_flagged, f"Evil log {f} was not flagged as EVIL."