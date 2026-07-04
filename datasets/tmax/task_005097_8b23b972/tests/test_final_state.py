# test_final_state.py
import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
ATTACKER_IP_FILE = "/home/user/attacker_ip.txt"
EXPECTED_IP = "192.168.1.42"

def test_attacker_ip_identified():
    assert os.path.exists(ATTACKER_IP_FILE), f"The file {ATTACKER_IP_FILE} does not exist."
    assert os.path.isfile(ATTACKER_IP_FILE), f"{ATTACKER_IP_FILE} is not a regular file."

    with open(ATTACKER_IP_FILE, 'r') as f:
        content = f.read().strip()

    assert content == EXPECTED_IP, f"Expected attacker IP {EXPECTED_IP}, but found '{content}'."

def test_compilation_and_execution():
    # Ensure we are in the correct directory
    assert os.path.exists(APP_DIR), f"Directory {APP_DIR} does not exist."

    # Clean and compile
    clean_proc = subprocess.run(["make", "clean"], cwd=APP_DIR, capture_output=True, text=True)
    assert clean_proc.returncode == 0, f"'make clean' failed:\n{clean_proc.stderr}"

    make_proc = subprocess.run(["make"], cwd=APP_DIR, capture_output=True, text=True)
    assert make_proc.returncode == 0, f"'make' failed to compile the code:\n{make_proc.stderr}"

    binary_path = os.path.join(APP_DIR, "packet_processor")
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} not found after 'make'."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

    pcap_path = os.path.join(APP_DIR, "traffic.pcap")
    assert os.path.exists(pcap_path), f"PCAP file {pcap_path} is missing."

    # Run the binary with a 2-second timeout
    try:
        run_proc = subprocess.run(
            [binary_path, pcap_path],
            cwd=APP_DIR,
            capture_output=True,
            text=True,
            timeout=2.0
        )
        assert run_proc.returncode == 0, (
            f"packet_processor failed with exit code {run_proc.returncode}.\n"
            f"STDOUT:\n{run_proc.stdout}\nSTDERR:\n{run_proc.stderr}"
        )
    except subprocess.TimeoutExpired:
        pytest.fail("packet_processor timed out after 2 seconds. The infinite loop bug is likely not fixed.")