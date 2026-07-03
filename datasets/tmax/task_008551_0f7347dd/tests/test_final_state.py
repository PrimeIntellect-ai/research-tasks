# test_final_state.py

import os
import stat
import hashlib
import pytest
import re

def test_phase1_suid_hashes():
    output_file = "/home/user/suid_hashes.txt"
    assert os.path.isfile(output_file), f"Phase 1 output file {output_file} is missing."

    bin_dir = "/home/user/fs_dump/bin"
    expected_lines = []

    # Find SUID files and compute hashes dynamically
    for root, _, files in os.walk(bin_dir):
        for file in files:
            filepath = os.path.join(root, file)
            st = os.stat(filepath)
            if st.st_mode & stat.S_ISUID:
                with open(filepath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                expected_lines.append(f"{file_hash}  {filepath}")

    expected_lines.sort()

    with open(output_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The SUID hashes file does not match the expected output or is not sorted correctly."

def test_phase2_redacted_environ():
    redacted_file = "/home/user/evidence/redacted_environ.txt"
    assert os.path.isfile(redacted_file), f"Phase 2 output file {redacted_file} is missing."

    expected_content = (
        "USER=admin\n"
        "PATH=/usr/bin:/bin\n"
        "PASSWORD=REDACTED\n"
        "HOME=/home/admin\n"
    )

    with open(redacted_file, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {redacted_file} is incorrect."

def test_phase2_hash_file():
    hash_file = "/home/user/evidence/hash.txt"
    redacted_file = "/home/user/evidence/redacted_environ.txt"

    assert os.path.isfile(hash_file), f"Phase 2 hash file {hash_file} is missing."
    assert os.path.isfile(redacted_file), f"Phase 2 redacted file {redacted_file} is missing."

    with open(redacted_file, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The hash in {hash_file} does not match the SHA-256 of {redacted_file}."

def test_phase2_c_program():
    c_source = "/home/user/evidence/extractor.c"
    c_binary = "/home/user/evidence/extractor"

    assert os.path.isfile(c_source), f"C source file {c_source} is missing."
    assert os.path.isfile(c_binary), f"Compiled binary {c_binary} is missing."

    st = os.stat(c_binary)
    assert st.st_mode & stat.S_IXUSR, f"The compiled binary {c_binary} is not executable."

def test_phase3_iptables_script():
    script_file = "/home/user/iptables_rule.sh"
    assert os.path.isfile(script_file), f"Phase 3 script {script_file} is missing."

    st = os.stat(script_file)
    assert st.st_mode & stat.S_IXUSR, f"The script {script_file} is not executable."

    with open(script_file, "r") as f:
        lines = f.readlines()

    iptables_commands = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

    assert len(iptables_commands) == 1, "The script must contain exactly one uncommented command."

    cmd = iptables_commands[0]

    # Check for required iptables components
    assert cmd.startswith("iptables"), "The command must start with 'iptables'."
    assert "-A INPUT" in cmd or "-I INPUT" in cmd, "The command must append or insert to the INPUT chain."
    assert "10.10.10.55" in cmd, "The command must target the IP 10.10.10.55."
    assert "1337" in cmd, "The command must target port 1337."
    assert "-j DROP" in cmd, "The command must jump to the DROP target."
    assert "-p tcp" in cmd or "--protocol tcp" in cmd, "The command must specify the TCP protocol."