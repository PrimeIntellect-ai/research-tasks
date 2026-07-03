# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_detector_exists():
    assert os.path.isfile("/home/user/detector"), "Detector executable missing at /home/user/detector"
    assert os.access("/home/user/detector", os.X_OK), "Detector is not executable"

def test_monitor_script_exists():
    assert os.path.isfile("/home/user/monitor.sh"), "Monitor script missing at /home/user/monitor.sh"

def test_cron_job_setup():
    cron_content = ""
    # Check user crontab
    result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
    if result.returncode == 0:
        cron_content += result.stdout

    # Also check system-wide cron just in case the user configured it there
    if os.path.isfile("/etc/crontab"):
        with open("/etc/crontab", "r") as f:
            cron_content += f.read()

    for cron_file in glob.glob("/etc/cron.d/*"):
        if os.path.isfile(cron_file):
            with open(cron_file, "r") as f:
                cron_content += f.read()

    assert "/home/user/monitor.sh" in cron_content, "Monitor script /home/user/monitor.sh is not scheduled in any cron configuration"

def test_adversarial_corpus_evil():
    evil_files = glob.glob("/app/corpus/evil/*.json")
    assert len(evil_files) > 0, "No evil corpus files found in /app/corpus/evil/"

    bypassed = []
    for f in evil_files:
        with open(f, 'r') as stdin_file:
            result = subprocess.run(["/home/user/detector"], stdin=stdin_file)
            if result.returncode != 1:
                bypassed.append(os.path.basename(f))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_adversarial_corpus_clean():
    clean_files = glob.glob("/app/corpus/clean/*.json")
    assert len(clean_files) > 0, "No clean corpus files found in /app/corpus/clean/"

    modified = []
    for f in clean_files:
        with open(f, 'r') as stdin_file:
            result = subprocess.run(["/home/user/detector"], stdin=stdin_file)
            if result.returncode != 0:
                modified.append(os.path.basename(f))

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified: {', '.join(modified)}"