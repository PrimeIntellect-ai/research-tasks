# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_nginx_backup_exists():
    backup_path = "/home/user/backup/nginx.conf.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist"

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/nginx_setup/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Missing Nginx config at {nginx_conf_path}"

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:8080;" in content, "Nginx config does not contain the fixed proxy_pass directive (8080)"
    assert "9999" not in content, "Nginx config still contains the old port 9999"

def test_rust_binary_exists():
    binary_path = "/home/user/bin/log-sanitizer"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist"
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable"

def test_adversarial_corpus_filtering():
    binary_path = "/home/user/bin/log-sanitizer"
    clean_corpus_dir = "/app/corpora/clean"
    evil_corpus_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_corpus_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_corpus_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_modified = []
    evil_bypassed = []

    for clean_file in clean_files:
        with open(clean_file, "r") as f:
            original_lines = f.readlines()

        with open(clean_file, "rb") as f:
            result = subprocess.run([binary_path], stdin=f, capture_output=True, text=True)

        output_lines = result.stdout.splitlines(keepends=True)
        if output_lines != original_lines:
            clean_modified.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        with open(evil_file, "r") as f:
            original_lines = f.readlines()

        with open(evil_file, "rb") as f:
            result = subprocess.run([binary_path], stdin=f, capture_output=True, text=True)

        output_lines = result.stdout.splitlines(keepends=True)

        # In evil files, lines containing malicious signatures must be dropped.
        # The signatures are ../, UNION SELECT, <script>
        signatures = ["../", "UNION SELECT", "<script>"]

        for orig_line in original_lines:
            has_sig = any(sig in orig_line for sig in signatures)
            if has_sig and orig_line in output_lines:
                if os.path.basename(evil_file) not in evil_bypassed:
                    evil_bypassed.append(os.path.basename(evil_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)