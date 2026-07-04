# test_final_state.py

import os
import glob
import subprocess
import time
import re

def test_classifier_adversarial_corpus():
    classifier_path = "/home/user/classifier"
    assert os.path.isfile(classifier_path), f"Classifier binary missing: {classifier_path}"
    assert os.access(classifier_path, os.X_OK), f"Classifier is not executable: {classifier_path}"

    evil_dir = "/home/user/corpus/evil"
    clean_dir = "/home/user/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.log"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.log"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([classifier_path, evil_file], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "EVIL":
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([classifier_path, clean_file], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Classifier failed corpus tests:\n" + "\n".join(errors)

def test_log_forwarding_flow():
    forwarder_script = "/home/user/forwarder.sh"
    assert os.path.isfile(forwarder_script), f"Forwarder script missing: {forwarder_script}"
    assert os.access(forwarder_script, os.X_OK), f"Forwarder script is not executable: {forwarder_script}"

    qemu_log = "/tmp/qemu.log"
    aggregated_log = "/tmp/aggregated.log"

    test_string = "VERIFICATION_STRING_1337"

    with open(qemu_log, "a") as f:
        f.write(f"\n{test_string}\n")

    time.sleep(2)

    assert os.path.isfile(aggregated_log), f"Aggregated log missing: {aggregated_log}"

    with open(aggregated_log, "r") as f:
        content = f.read()

    assert test_string in content, f"Test string '{test_string}' not found in {aggregated_log}. Forwarding pipeline is not working."

def test_logrotate_config():
    config_path = "/home/user/qemu-logrotate.conf"
    assert os.path.isfile(config_path), f"Logrotate config missing: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    assert re.search(r"size\s+1M", content), "Logrotate config missing 'size 1M'"
    assert re.search(r"rotate\s+5", content), "Logrotate config missing 'rotate 5'"
    assert "compress" in content, "Logrotate config missing 'compress'"
    assert "prerotate" in content, "Logrotate config missing 'prerotate' block"
    assert "/home/user/classifier" in content, "Logrotate config prerotate block missing classifier invocation"