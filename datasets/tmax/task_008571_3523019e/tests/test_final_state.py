# test_final_state.py

import os
import subprocess
import pytest

def test_leak_packet_identified():
    """Check if the leak packet number was correctly identified and written to leak_packet.txt."""
    file_path = "/home/user/leak_packet.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "73", f"Expected packet number 73 in {file_path}, but got '{content}'."

def test_network_parser_fixed_exists():
    """Check if the fixed script was saved correctly."""
    file_path = "/home/user/network_parser_fixed.py"
    assert os.path.isfile(file_path), f"Fixed script {file_path} does not exist."

def test_network_parser_fixed_execution():
    """Check if the fixed script runs and reports 0 leaked buffer items."""
    script_path = "/home/user/network_parser_fixed.py"
    pcap_path = "/home/user/capture.pcap"

    assert os.path.isfile(script_path), f"Fixed script {script_path} does not exist."
    assert os.path.isfile(pcap_path), f"PCAP file {pcap_path} does not exist."

    try:
        result = subprocess.run(
            ["python3", script_path, pcap_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing {script_path} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Executing {script_path} timed out. There might still be an unbounded loop or memory issue.")

    output = result.stdout
    assert "Leaked buffer items: 0" in output, f"Expected 'Leaked buffer items: 0' in output, but got:\n{output}"