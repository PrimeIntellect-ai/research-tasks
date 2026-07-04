# test_final_state.py
import os
import subprocess

def test_upload_handler_patched():
    handler_path = "/home/user/upload_handler.sh"
    assert os.path.isfile(handler_path), f"File {handler_path} is missing."

    # Clean up before test
    malicious_target = "/home/user/test_upload.txt"
    safe_target = "/home/user/uploads/test_upload.txt"
    if os.path.exists(malicious_target):
        os.remove(malicious_target)
    if os.path.exists(safe_target):
        os.remove(safe_target)

    env = os.environ.copy()
    env["FILENAME"] = "../../../home/user/test_upload.txt"

    process = subprocess.Popen(
        [handler_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    process.communicate(input=b"test_content")

    assert not os.path.exists(malicious_target), (
        f"Path traversal vulnerability still exists! File was written to {malicious_target}"
    )
    assert os.path.exists(safe_target), (
        f"The script failed to write the file to the safe directory {safe_target}"
    )

    with open(safe_target, "r") as f:
        assert f.read() == "test_content", "The uploaded file content does not match the input."

def test_ssh_keys_remediated():
    keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(keys_path), f"File {keys_path} is missing."

    with open(keys_path, "r") as f:
        content = f.read()

    assert "LegitimateKey123" in content, "The legitimate SSH key was removed from authorized_keys."
    assert "attacker@evil.corp" not in content, "The attacker's SSH key is still present in authorized_keys."

def test_crack_script_exists():
    script_path = "/home/user/crack.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing. You need to write the brute-force script."

def test_extracted_payload_zip_exists():
    zip_path = "/home/user/extracted_payload.zip"
    assert os.path.isfile(zip_path), f"File {zip_path} is missing."

    # Check if it's a valid zip file format by reading the magic number
    with open(zip_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"PK\x03\x04", f"File {zip_path} does not appear to be a valid ZIP archive."

def test_malware_hash_correct():
    hash_file = "/home/user/malware_hash.txt"
    expected_hash_file = "/home/user/expected_hash.txt"

    assert os.path.isfile(hash_file), f"File {hash_file} is missing."
    assert os.path.isfile(expected_hash_file), f"File {expected_hash_file} is missing (environment issue)."

    with open(hash_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_hash_file, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, (
        f"The hash in {hash_file} does not match the expected hash of the malware."
    )