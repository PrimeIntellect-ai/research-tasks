# test_final_state.py

import os
import subprocess
import glob
import re
import pytest

def test_incident_report():
    """Test that the incident report contains the correct frame number."""
    report_path = "/home/user/incident_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "142", f"Expected incident report to contain '142', but found '{content}'."

def test_nginx_proxy_config():
    """Test that the Nginx proxy configuration meets the requirements."""
    config_path = "/home/user/proxy.conf"
    assert os.path.isfile(config_path), f"File {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    # Check for listening on port 8080
    assert re.search(r"listen\s+8080\b", content), "Nginx config does not listen on port 8080."

    # Check for proxy_pass
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:8081/?\s*;", content), "Nginx config does not proxy to http://127.0.0.1:8081."

    # Check for allow and deny
    assert re.search(r"allow\s+127\.0\.0\.1\s*;", content), "Nginx config missing 'allow 127.0.0.1;' directive."
    assert re.search(r"deny\s+all\s*;", content), "Nginx config missing 'deny all;' directive."

def test_adversarial_corpus():
    """Test the filter_video.py script against the clean and evil corpora."""
    script_path = "/home/user/filter_video.py"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_videos = glob.glob(os.path.join(clean_dir, "*.mp4"))
    evil_videos = glob.glob(os.path.join(evil_dir, "*.mp4"))

    assert len(clean_videos) > 0, "No clean videos found in corpus."
    assert len(evil_videos) > 0, "No evil videos found in corpus."

    failed_clean = []
    failed_evil = []

    # Test clean corpus (should exit 0)
    for video in clean_videos:
        result = subprocess.run(
            ["python3", script_path, video],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            failed_clean.append(os.path.basename(video))

    # Test evil corpus (should exit 1)
    for video in evil_videos:
        result = subprocess.run(
            ["python3", script_path, video],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 1:
            failed_evil.append(os.path.basename(video))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_videos)} clean videos modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_videos)} evil videos bypassed: {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)