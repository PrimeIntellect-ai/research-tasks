# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_config_updated():
    config_path = "/home/user/gateway/config/settings.toml"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing"
    with open(config_path, "r") as f:
        content = f.read()
    assert "upstream_port = 8081" in content, "Config file was not updated to upstream_port = 8081"

def test_deployment_pipeline():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deploy script {deploy_script} is missing"
    assert os.access(deploy_script, os.X_OK), f"Deploy script {deploy_script} is not executable"

    current_symlink = "/home/user/deploy/current"
    assert os.path.islink(current_symlink), f"{current_symlink} is not a symlink"

    payload_filter = os.path.join(current_symlink, "payload_filter")
    gateway_server = os.path.join(current_symlink, "gateway_server")

    assert os.path.isfile(payload_filter), f"Compiled binary {payload_filter} is missing"
    assert os.path.isfile(gateway_server), f"Compiled binary {gateway_server} is missing"

def test_adversarial_corpus():
    payload_filter = "/home/user/deploy/current/payload_filter"
    assert os.path.isfile(payload_filter), "payload_filter binary missing, cannot test corpus"

    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run([payload_filter, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run([payload_filter, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    assert not error_msgs, " | ".join(error_msgs)