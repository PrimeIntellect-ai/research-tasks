# test_final_state.py
import os
import subprocess
import urllib.parse
import pytest

def test_binary_exists():
    binary_path = "/home/user/workspace/sanitizer"
    assert os.path.isfile(binary_path), f"Binary {binary_path} not found."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_config_updated():
    config_path = "/home/user/workspace/config.env"
    assert os.path.isfile(config_path), f"{config_path} not found."
    with open(config_path, "r") as f:
        content = f.read()
    assert "FILTER_BIN=/home/user/workspace/sanitizer" in content, "config.env not updated correctly to point to the new binary."

def test_report_exists():
    report_path = "/home/user/workspace/test_report.log"
    assert os.path.isfile(report_path), f"{report_path} not found. Did you run the generate_report.sh script?"

def test_clean_corpus():
    binary_path = "/home/user/workspace/sanitizer"
    clean_path = "/app/corpus/clean.txt"
    assert os.path.isfile(clean_path), f"{clean_path} not found."

    with open(clean_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    failed_lines = []
    for line in lines:
        expected_decoded = urllib.parse.unquote_plus(line)
        expected_stdout = f"ACCEPTED: {expected_decoded}"

        proc = subprocess.run([binary_path], input=line.encode('utf-8'), capture_output=True)
        stdout = proc.stdout.decode('utf-8', errors='replace').strip()

        if proc.returncode != 0 or stdout != expected_stdout:
            failed_lines.append(line)

    assert not failed_lines, f"{len(failed_lines)} of {len(lines)} clean modified/rejected. Offending lines: {failed_lines[:5]}"

def test_evil_corpus():
    binary_path = "/home/user/workspace/sanitizer"
    evil_path = "/app/corpus/evil.txt"
    assert os.path.isfile(evil_path), f"{evil_path} not found."

    with open(evil_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    failed_lines = []
    for line in lines:
        proc = subprocess.run([binary_path], input=line.encode('utf-8'), capture_output=True)
        stdout = proc.stdout.decode('utf-8', errors='replace').strip()

        if proc.returncode != 1 or stdout != "REJECTED":
            failed_lines.append(line)

    assert not failed_lines, f"{len(failed_lines)} of {len(lines)} evil bypassed. Offending lines: {failed_lines[:5]}"