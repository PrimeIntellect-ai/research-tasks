# test_final_state.py
import os
import json
import subprocess
import pytest
import re

def test_doc_filter_binary_exists():
    binary_path = "/home/user/doc_filter"
    assert os.path.isfile(binary_path), f"Document filter binary missing: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Document filter binary is not executable: {binary_path}"

def test_doc_filter_corpus():
    binary_path = "/home/user/doc_filter"
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(f)

    evil_bypassed = []
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        result = subprocess.run([binary_path, filepath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(f)

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, "Corpus verification failed:\n" + "\n".join(errors)

def test_uploader_config():
    config_path = "/home/user/services/uploader/config.json"
    assert os.path.isfile(config_path), f"Uploader config missing: {config_path}"

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Uploader config is not valid JSON: {config_path}")

    assert config.get("FILTER_BIN") == "/home/user/doc_filter", "FILTER_BIN not set correctly"
    assert config.get("PUBLISH_DIR") == "/home/user/docs_published", "PUBLISH_DIR not set correctly"
    assert config.get("BACKUP_URL") == "http://127.0.0.1:5001/backup", "BACKUP_URL not set correctly"

def test_nginx_config():
    config_path = "/home/user/services/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config missing: {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Look for a server block listening on 8080 and its root directive
    # This is a basic regex to find the root directive inside the server block for 8080
    # It assumes standard nginx formatting
    server_8080_pattern = re.compile(r'listen\s+8080\s*;.*?root\s+/home/user/docs_published\s*;', re.DOTALL)

    # Alternatively, just check if the root is set to the right path
    assert "/home/user/docs_published" in content, "Nginx config does not contain the correct root path"

def test_file_operations_and_linking():
    publish_dir = "/home/user/docs_published"
    assert os.path.isdir(publish_dir), f"Publish directory missing: {publish_dir}"

    symlink_path = os.path.join(publish_dir, "index.md")
    assert os.path.islink(symlink_path), f"Symlink missing or not a symlink: {symlink_path}"

    target = os.readlink(symlink_path)
    # The target can be absolute or relative, but it must resolve to /home/user/docs_published/home.md
    expected_target = "/home/user/docs_published/home.md"

    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(publish_dir, target))

    assert target == expected_target, f"Symlink points to {target}, expected {expected_target}"