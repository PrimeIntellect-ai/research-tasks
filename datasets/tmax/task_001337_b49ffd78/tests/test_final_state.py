# test_final_state.py

import os
import re
import stat
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deploy script {deploy_script} does not exist."
    st = os.stat(deploy_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deploy script {deploy_script} is not executable."

def test_tunnel_cmd_content():
    tunnel_file = "/home/user/tunnel_cmd.txt"
    assert os.path.isfile(tunnel_file), f"Tunnel command file {tunnel_file} does not exist."

    with open(tunnel_file, "r") as f:
        content = f.read().strip()

    # Regex match for -L 8080:localhost:9090 (or 127.0.0.1) and -N and -f
    assert re.search(r'-L\s*8080:(127\.0\.0\.1|localhost):9090', content), f"Missing or incorrect port forwarding in {tunnel_file}."
    assert re.search(r'-N', content), f"Missing -N flag in {tunnel_file}."
    assert re.search(r'-f', content), f"Missing -f flag in {tunnel_file}."

def test_tamper_frames_content():
    tamper_file = "/home/user/tamper_frames.txt"
    assert os.path.isfile(tamper_file), f"Tamper frames file {tamper_file} does not exist."

    with open(tamper_file, "r") as f:
        content = f.read().strip()

    assert content == "42,43,44,45,46", f"Expected '42,43,44,45,46' in {tamper_file}, got '{content}'."

def test_sanitizer_bin_corpus():
    sanitizer_bin = "/home/user/sanitizer_bin"
    assert os.path.isfile(sanitizer_bin), f"Sanitizer binary {sanitizer_bin} does not exist. Did deploy.sh compile it?"

    st = os.stat(sanitizer_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"Sanitizer binary {sanitizer_bin} is not executable."

    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    clean_failed = []
    evil_failed = []

    # Test clean corpus
    if os.path.isdir(clean_corpus_dir):
        for filename in os.listdir(clean_corpus_dir):
            filepath = os.path.join(clean_corpus_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    payload = f.read()
                result = subprocess.run([sanitizer_bin], input=payload, capture_output=True)
                if result.returncode != 0:
                    clean_failed.append(filename)

    # Test evil corpus
    if os.path.isdir(evil_corpus_dir):
        for filename in os.listdir(evil_corpus_dir):
            filepath = os.path.join(evil_corpus_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    payload = f.read()
                result = subprocess.run([sanitizer_bin], input=payload, capture_output=True)
                if result.returncode == 0:
                    evil_failed.append(filename)

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} clean payloads rejected (expected accepted): {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} evil payloads accepted (expected rejected): {', '.join(evil_failed)}")

    assert not error_messages, " | ".join(error_messages)