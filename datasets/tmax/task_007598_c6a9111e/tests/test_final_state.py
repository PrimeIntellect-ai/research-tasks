# test_final_state.py

import os
import subprocess
import pytest

def test_c2_domain_extracted():
    c2_domain_path = "/home/user/c2_domain.txt"
    assert os.path.isfile(c2_domain_path), f"The file {c2_domain_path} does not exist."

    with open(c2_domain_path, "r") as f:
        content = f.read().strip()

    assert content == "super-evil.com", f"Expected 'super-evil.com' in {c2_domain_path}, found '{content}'"

def test_minimal_decoder_exists_and_executable():
    decoder_path = "/home/user/minimal_decoder.sh"
    assert os.path.isfile(decoder_path), f"The file {decoder_path} does not exist."
    assert os.access(decoder_path, os.X_OK), f"The file {decoder_path} is not executable."

def test_minimal_decoder_functionality():
    decoder_path = "/home/user/minimal_decoder.sh"

    # Test case 1: "74736574" -> "test"
    try:
        result1 = subprocess.run([decoder_path, "74736574"], capture_output=True, text=True, timeout=5)
        assert result1.returncode == 0, f"minimal_decoder.sh failed with return code {result1.returncode}"
        assert result1.stdout.strip() == "test", f"Expected 'test' from minimal_decoder.sh '74736574', got '{result1.stdout.strip()}'"
    except subprocess.TimeoutExpired:
        pytest.fail("minimal_decoder.sh timed out on input '74736574'. It might contain an infinite loop.")

    # Test case 2: "646162" -> "bad"
    try:
        result2 = subprocess.run([decoder_path, "646162"], capture_output=True, text=True, timeout=5)
        assert result2.returncode == 0, f"minimal_decoder.sh failed with return code {result2.returncode}"
        assert result2.stdout.strip() == "bad", f"Expected 'bad' from minimal_decoder.sh '646162', got '{result2.stdout.strip()}'"
    except subprocess.TimeoutExpired:
        pytest.fail("minimal_decoder.sh timed out on input '646162'. It might contain an infinite loop.")

def test_suspicious_dropper_fixed():
    dropper_path = "/home/user/suspicious_dropper.sh"
    assert os.path.isfile(dropper_path), f"The file {dropper_path} does not exist."

    try:
        result = subprocess.run(["bash", dropper_path], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"suspicious_dropper.sh failed with return code {result.returncode}"
        assert "super-evil.com" in result.stdout, "suspicious_dropper.sh did not output the expected domain."
    except subprocess.TimeoutExpired:
        pytest.fail("suspicious_dropper.sh timed out. The infinite loop bug was not fixed.")