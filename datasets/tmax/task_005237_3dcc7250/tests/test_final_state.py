# test_final_state.py

import os
import subprocess
import pytest
import re

def test_part1_vendored_package_installed():
    """Verify that the mobile_asset_builder package is installed and works correctly."""
    try:
        import mobile_asset_builder
    except ImportError:
        pytest.fail("mobile_asset_builder is not installed in the Python environment.")

    try:
        result = mobile_asset_builder.process("test")
        assert result == "test_asset", f"Expected 'test_asset', got '{result}'"
    except Exception as e:
        pytest.fail(f"mobile_asset_builder.process failed: {e}")

def test_part2_manifest_sanitizer():
    """Verify the sanitizer script correctly accepts clean and rejects evil files."""
    script_path = "/home/user/sanitizer.py"
    assert os.path.isfile(script_path), f"Sanitizer script missing at {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)] if os.path.isdir(clean_dir) else []
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)] if os.path.isdir(evil_dir) else []

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_part3_reverse_proxy_config():
    """Verify the Nginx configuration file contains the required directives."""
    config_path = "/home/user/proxy.conf"
    assert os.path.isfile(config_path), f"Nginx config missing at {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'#.*', '', content)

    # Check listen
    assert re.search(r'listen\s+8080\s*;', content), "Missing or incorrect 'listen 8080;' directive."

    # Check proxy_pass
    assert re.search(r'proxy_pass\s+http://127\.0\.0\.1:9000/?\s*;', content), "Missing or incorrect 'proxy_pass http://127.0.0.1:9000;' directive."

    # Check proxy_set_header
    assert re.search(r'proxy_set_header\s+X-Mobile-Pipeline\s+["\']?secured["\']?\s*;', content, re.IGNORECASE), "Missing or incorrect 'proxy_set_header X-Mobile-Pipeline secured;' directive."