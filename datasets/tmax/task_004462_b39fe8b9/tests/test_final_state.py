# test_final_state.py

import os
import subprocess
import random
import time
import urllib.request
import urllib.error
import glob
import configparser

def test_config_updated():
    config_path = "/home/user/artifact_manager/config.ini"
    assert os.path.isfile(config_path), f"Missing {config_path}"

    config = configparser.ConfigParser()
    config.read(config_path)

    # Check if section exists, might be 'DEFAULT' or some other section. 
    # Just read as text to be safe if section is unknown.
    with open(config_path, "r") as f:
        content = f.read()

    assert "queue_type = redis" in content or "queue_type=redis" in content.replace(" ", ""), \
        "config.ini does not have 'queue_type = redis'"
    assert "redis://127.0.0.1:6379/0" in content, \
        "config.ini does not have the correct redis_url"

def test_fuzz_equivalence_elf_parser():
    agent_parser = "/home/user/artifact_manager/elf_parser.py"
    oracle_parser = "/app/oracle_parser.py"

    assert os.path.isfile(agent_parser), f"Agent parser missing at {agent_parser}"
    assert os.access(agent_parser, os.X_OK), f"Agent parser {agent_parser} is not executable"
    assert os.path.isfile(oracle_parser), f"Oracle parser missing at {oracle_parser}"

    # Collect ELF files
    elf_candidates = []
    for d in ["/usr/bin", "/usr/lib"]:
        for root, _, files in os.walk(d):
            for f in files:
                filepath = os.path.join(root, f)
                if os.path.isfile(filepath) and not os.path.islink(filepath):
                    try:
                        with open(filepath, 'rb') as fd:
                            if fd.read(4) == b'\x7fELF':
                                elf_candidates.append(filepath)
                    except Exception:
                        pass

    random.seed(42)
    test_files = random.sample(elf_candidates, min(50, len(elf_candidates)))
    assert len(test_files) > 0, "No ELF files found for testing"

    for elf_file in test_files:
        agent_proc = subprocess.run(
            ["python3", agent_parser, elf_file], 
            capture_output=True, text=True
        )
        oracle_proc = subprocess.run(
            ["python3", oracle_parser, elf_file], 
            capture_output=True, text=True
        )

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on {elf_file}. Agent: {agent_proc.returncode}, Oracle: {oracle_proc.returncode}"

        if oracle_proc.returncode == 0:
            assert agent_out == oracle_out, \
                f"Output mismatch on {elf_file}.\nExpected: {oracle_out}\nGot: {agent_out}"

def test_end_to_end_upload_and_symlink():
    # Test file
    test_elf = "/usr/bin/ls"
    assert os.path.isfile(test_elf), f"Test file {test_elf} missing"

    # Use curl to upload
    cmd = ["curl", "-s", "-F", f"file=@{test_elf}", "http://127.0.0.1:5000/upload"]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    # Wait for worker to process
    time.sleep(3)

    # Check if symlink exists
    # Architecture of /usr/bin/ls is likely EM_X86_64 or EM_AARCH64
    # We can run the oracle to get the exact architecture
    oracle_parser = "/app/oracle_parser.py"
    oracle_proc = subprocess.run(
        ["python3", oracle_parser, test_elf], 
        capture_output=True, text=True
    )
    assert oracle_proc.returncode == 0, "Oracle failed to parse test file"

    arch = oracle_proc.stdout.strip().split("|")[0]

    expected_symlink = f"/home/user/artifact_manager/curated/{arch}/ls"
    assert os.path.islink(expected_symlink), f"Expected symlink at {expected_symlink} was not created"

    target = os.readlink(expected_symlink)
    assert target.endswith("/ls") and "uploads" in target, \
        f"Symlink {expected_symlink} does not point to an uploaded file in uploads/. Points to: {target}"