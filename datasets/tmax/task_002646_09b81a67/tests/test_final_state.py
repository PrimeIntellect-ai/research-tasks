# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_setup_ci_script():
    setup_script = "/home/user/setup_ci.sh"
    assert os.path.isfile(setup_script), f"Setup script {setup_script} does not exist."

    # Execute the setup script
    result = subprocess.run(["bash", setup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Setup script failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_filter_binary_exists():
    binary_path = "/home/user/netfilter/filter"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_systemd_service_file():
    service_path = "/home/user/netfilter.service"
    assert os.path.isfile(service_path), f"Service file {service_path} does not exist."

    with open(service_path, "r") as f:
        content = f.read()

    assert "[Unit]" in content, f"Service file {service_path} is missing [Unit] section."
    assert "[Service]" in content, f"Service file {service_path} is missing [Service] section."
    assert "ExecStart" in content, f"Service file {service_path} is missing ExecStart directive."

def test_adversarial_corpus_filtering():
    binary_path = "/home/user/netfilter/filter"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures[:10])}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures[:10])}")

    assert not clean_failures and not evil_failures, "Corpus filtering failed:\n" + "\n".join(error_msgs)