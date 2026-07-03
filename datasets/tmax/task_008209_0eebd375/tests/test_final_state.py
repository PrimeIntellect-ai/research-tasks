# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist. Did you save the bad commit hash?"
    assert os.path.isfile(expected_file), f"{expected_file} is missing, cannot verify."

    with open(bad_commit_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {bad_commit_file} ({actual_hash}) does not match the expected bad commit ({expected_hash})."

def test_parse_pcap_fixes():
    script_path = "/home/user/repo/parse_pcap.py"
    pcap_path = "/home/user/test_traffic.pcap"

    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.path.isfile(pcap_path), f"{pcap_path} does not exist."

    try:
        output = subprocess.check_output(
            ["python3", script_path, pcap_path],
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {script_path} failed with exit code {e.returncode}. Output:\n{e.output}")

    assert "Precision loss detected" not in output, "The script still detects precision loss. The regex/parsing fix is incomplete."
    assert "Parsed price:" in output, "The script did not print any parsed prices. Make sure it successfully extracts them."

def test_mre_script():
    mre_path = "/home/user/mre.py"

    assert os.path.isfile(mre_path), f"{mre_path} does not exist. Did you create the minimal reproducible example?"

    with open(mre_path, "r") as f:
        content = f.read()

    assert "PRICE=" in content, f"The script {mre_path} does not contain the hardcoded payload 'PRICE='."

    try:
        subprocess.check_call(
            ["python3", mre_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pytest.fail(f"Running {mre_path} failed. Ensure it is a valid Python script that executes without errors.")