# test_final_state.py

import os
import re
import subprocess
import tempfile
import yaml
import pytest

def parse_records(text):
    pattern = r'(?m)^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'
    starts = [m.start() for m in re.finditer(pattern, text)]
    if not starts:
        return []
    records = []
    for i in range(len(starts)):
        start_idx = starts[i]
        end_idx = starts[i+1] if i + 1 < len(starts) else len(text)
        records.append(text[start_idx:end_idx])
    return records

def test_webapp_config():
    path = "/home/user/app/webapp/config.yaml"
    assert os.path.exists(path), f"Config file {path} missing."
    with open(path, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError:
            content = f.read()
            assert "log_dir: /home/user/logs/raw/" in content, "log_dir not updated to /home/user/logs/raw/"
            return
    assert config.get('log_dir') == '/home/user/logs/raw/', "log_dir in config.yaml must be /home/user/logs/raw/"

def test_nginx_config():
    path = "/home/user/app/nginx.conf"
    assert os.path.exists(path), f"Nginx config {path} missing."
    with open(path, 'r') as f:
        content = f.read()
    assert re.search(r'(?i)X-Sanitizer-Enabled[\s:]+true', content) or "X-Sanitizer-Enabled" in content, \
        "Nginx config is missing the X-Sanitizer-Enabled header injection."

def test_adversarial_corpus():
    binary = "/home/user/log_sanitizer"
    assert os.path.isfile(binary), f"Binary {binary} not found."
    assert os.access(binary, os.X_OK), f"Binary {binary} is not executable."

    clean_in = "/home/user/verifier/clean_corpus"
    evil_in = "/home/user/verifier/evil_corpus"

    assert os.path.isdir(clean_in), f"Clean corpus dir {clean_in} missing."
    assert os.path.isdir(evil_in), f"Evil corpus dir {evil_in} missing."

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run on clean corpus
        res_clean = subprocess.run([binary, clean_in, clean_out], capture_output=True, text=True)
        assert res_clean.returncode == 0, f"Binary failed on clean corpus:\n{res_clean.stderr}"

        # Run on evil corpus
        res_evil = subprocess.run([binary, evil_in, evil_out], capture_output=True, text=True)
        assert res_evil.returncode == 0, f"Binary failed on evil corpus:\n{res_evil.stderr}"

        # Check clean corpus
        clean_modified = []
        clean_files = 0
        for root, _, files in os.walk(clean_in):
            for file in files:
                if not file.endswith('.log'):
                    continue
                clean_files += 1
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(in_path, clean_in)
                out_path = os.path.join(clean_out, rel_path)

                if not os.path.exists(out_path):
                    clean_modified.append(file)
                    continue

                with open(in_path, 'r') as f:
                    in_text = f.read()
                with open(out_path, 'r') as f:
                    out_text = f.read()

                if in_text != out_text:
                    clean_modified.append(file)

        # Check evil corpus
        evil_bypassed = []
        evil_files = 0
        for root, _, files in os.walk(evil_in):
            for file in files:
                if not file.endswith('.log'):
                    continue
                evil_files += 1
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(in_path, evil_in)
                out_path = os.path.join(evil_out, rel_path)

                with open(in_path, 'r') as f:
                    in_text = f.read()

                in_records = parse_records(in_text)
                expected_records = [r for r in in_records if "[SPAM-MODULE]" not in r]
                expected_text = "".join(expected_records)

                if not os.path.exists(out_path):
                    if expected_text:
                        evil_bypassed.append(file)
                    continue

                with open(out_path, 'r') as f:
                    out_text = f.read()

                if out_text != expected_text:
                    evil_bypassed.append(file)

        errors = []
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {clean_files} clean modified: {', '.join(clean_modified)}")
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {evil_files} evil bypassed: {', '.join(evil_bypassed)}")

        if errors:
            pytest.fail(" | ".join(errors))