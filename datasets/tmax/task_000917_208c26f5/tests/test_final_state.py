# test_final_state.py

import os
import subprocess
import socket
import pytest

def test_app_mount_service():
    """Verify that the app-mount service is active and the directory is mounted."""
    res = subprocess.run(
        ["systemctl", "--user", "is-active", "app-mount.service"],
        capture_output=True, text=True
    )
    assert res.stdout.strip() == "active", "app-mount.service is not active"

    # Verify that bindfs actually mounted the directory
    assert os.path.ismount("/home/user/app/config_mount"), "/home/user/app/config_mount is not mounted"

def test_redis_tunnel_service():
    """Verify that the redis-tunnel service is active and port 9000 is open."""
    res = subprocess.run(
        ["systemctl", "--user", "is-active", "redis-tunnel.service"],
        capture_output=True, text=True
    )
    assert res.stdout.strip() == "active", "redis-tunnel.service is not active"

    # Check if port 9000 is listening locally
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9000))
    sock.close()
    assert result == 0, "Port 9000 is not listening (SSH tunnel might be down)"

def test_go_binary_exists():
    """Verify that the Go program was compiled to the correct location."""
    binary_path = "/home/user/app/filter/metric_filter"
    assert os.path.isfile(binary_path), f"Go binary {binary_path} is missing"
    assert os.access(binary_path, os.X_OK), f"Go binary {binary_path} is not executable"

def test_adversarial_corpus():
    """
    Test the Go binary against the clean and evil corpora.
    Clean lines must be preserved exactly.
    Evil lines must be omitted entirely.
    """
    binary_path = "/home/user/app/filter/metric_filter"
    evil_corpus_path = "/home/user/corpus/evil_metrics.jsonl"
    clean_corpus_path = "/home/user/corpus/clean_metrics.jsonl"

    assert os.path.isfile(evil_corpus_path), f"Missing evil corpus: {evil_corpus_path}"
    assert os.path.isfile(clean_corpus_path), f"Missing clean corpus: {clean_corpus_path}"

    # Process Clean Corpus
    with open(clean_corpus_path, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    clean_failed = []
    for line in clean_lines:
        res = subprocess.run([binary_path], input=line, capture_output=True, text=True)
        out = res.stdout.strip()
        if out != line:
            clean_failed.append(line)

    # Process Evil Corpus
    with open(evil_corpus_path, "r") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    evil_failed = []
    for line in evil_lines:
        res = subprocess.run([binary_path], input=line, capture_output=True, text=True)
        out = res.stdout.strip()
        if out != "":
            evil_failed.append(line)

    err_msg = []
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} of {len(evil_lines)} evil bypassed")
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} of {len(clean_lines)} clean modified")

    if err_msg:
        pytest.fail(" | ".join(err_msg) + f". Offending clean: {clean_failed[:3]}..., Offending evil: {evil_failed[:3]}...")