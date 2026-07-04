# test_final_state.py

import os
import re
import glob
import subprocess
import pytest

def test_nginx_config():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for listen 80
    assert re.search(r"listen\s+80\s*;", content), "Nginx config does not correctly specify 'listen 80;'."

    # Check for proxy_pass to 127.0.0.1:8080
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:8080\s*;", content), "Nginx config does not correctly specify 'proxy_pass http://127.0.0.1:8080;'."

def test_sanitiser_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    cargo_dir = "/home/user/sanitiser"
    assert os.path.isdir(cargo_dir), f"Rust project directory missing at {cargo_dir}"

    # Pre-build the project to avoid compilation output mixing or timeouts during individual runs
    build_res = subprocess.run(["cargo", "build"], cwd=cargo_dir, capture_output=True)
    assert build_res.returncode == 0, f"Failed to build Rust project in {cargo_dir}:\n{build_res.stderr.decode()}"

    clean_failed = []
    evil_bypassed = []

    for cf in clean_files:
        res = subprocess.run(["cargo", "run", "--quiet", "--", cf], cwd=cargo_dir, capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run(["cargo", "run", "--quiet", "--", ef], cwd=cargo_dir, capture_output=True)
        # Exit code 0 means the evil payload was incorrectly accepted
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))