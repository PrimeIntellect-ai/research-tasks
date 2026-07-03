# test_final_state.py
import os
import stat
import json
import subprocess
import hashlib

def test_ssh_key_rotation():
    ssh_dir = "/home/user/.ssh"
    id_rsa = os.path.join(ssh_dir, "id_rsa")
    id_rsa_pub = os.path.join(ssh_dir, "id_rsa.pub")
    id_ed25519 = os.path.join(ssh_dir, "id_ed25519")
    id_ed25519_pub = os.path.join(ssh_dir, "id_ed25519.pub")
    auth_keys = os.path.join(ssh_dir, "authorized_keys")

    assert not os.path.exists(id_rsa), "Old id_rsa key was not deleted."
    assert not os.path.exists(id_rsa_pub), "Old id_rsa.pub key was not deleted."

    assert os.path.exists(id_ed25519), "New id_ed25519 key was not generated."
    assert os.path.exists(id_ed25519_pub), "New id_ed25519.pub key was not generated."

    with open(id_ed25519_pub, 'r') as f:
        pub_key_content = f.read().strip()

    assert os.path.exists(auth_keys), "authorized_keys file is missing."
    with open(auth_keys, 'r') as f:
        auth_keys_content = f.read().strip()

    assert auth_keys_content == pub_key_content, "authorized_keys does not exactly match the new id_ed25519 public key."

    # Check permissions
    ssh_dir_stat = os.stat(ssh_dir)
    assert stat.S_IMODE(ssh_dir_stat.st_mode) == 0o700, ".ssh directory permissions are not 700."

    auth_keys_stat = os.stat(auth_keys)
    assert stat.S_IMODE(auth_keys_stat.st_mode) == 0o600, "authorized_keys permissions are not 600."

def test_tampered_log():
    log_path = "/home/user/app/tampered.log"
    assert os.path.exists(log_path), "tampered.log was not created."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"tampered.log should contain exactly one entry, found {len(lines)}."
    assert lines[0] == "doc3.txt", f"tampered.log should contain 'doc3.txt', found '{lines[0]}'."

def test_encryption_and_integrity():
    app_dir = "/home/user/app"
    uploads_dir = os.path.join(app_dir, "uploads")
    new_key_path = os.path.join(app_dir, "new_key.key")
    hashes_path = os.path.join(app_dir, "file_hashes.json")

    assert os.path.exists(new_key_path), "new_key.key was not created."

    assert os.path.exists(os.path.join(uploads_dir, "doc1.txt")), "doc1.txt is missing from uploads."
    assert os.path.exists(os.path.join(uploads_dir, "doc2.txt")), "doc2.txt is missing from uploads."
    assert not os.path.exists(os.path.join(uploads_dir, "doc3.txt")), "doc3.txt should have been deleted."

    with open(hashes_path, 'r') as f:
        original_hashes = json.load(f)

    # Use a subprocess to decrypt to avoid third-party imports in the test file
    script = f"""
import sys
from cryptography.fernet import Fernet

try:
    with open('{new_key_path}', 'rb') as f:
        key = f.read()
    fernet = Fernet(key)

    with open('{os.path.join(uploads_dir, "doc1.txt")}', 'rb') as f:
        doc1 = fernet.decrypt(f.read())
    with open('{os.path.join(uploads_dir, "doc2.txt")}', 'rb') as f:
        doc2 = fernet.decrypt(f.read())

    sys.stdout.buffer.write(doc1 + b'|SPLIT|' + doc2)
except Exception as e:
    sys.stderr.write(str(e))
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True)
    assert result.returncode == 0, f"Failed to decrypt files with new_key.key. Error: {result.stderr.decode()}"

    decrypted_content = result.stdout.split(b'|SPLIT|')
    assert len(decrypted_content) == 2, "Failed to parse decrypted content."

    doc1_hash = hashlib.sha256(decrypted_content[0]).hexdigest()
    doc2_hash = hashlib.sha256(decrypted_content[1]).hexdigest()

    assert doc1_hash == original_hashes.get("doc1.txt"), "doc1.txt content hash does not match original."
    assert doc2_hash == original_hashes.get("doc2.txt"), "doc2.txt content hash does not match original."

def test_app_firewall_policy():
    app_path = "/home/user/app/app.py"
    assert os.path.exists(app_path), "app.py is missing."

    with open(app_path, 'r') as f:
        content = f.read()

    assert "before_request" in content, "before_request hook is missing in app.py."
    assert "request.remote_addr" in content, "request.remote_addr is not checked in app.py."
    assert "127.0.0.1" in content, "127.0.0.1 is not present in the firewall logic."
    assert "abort(403)" in content or "abort(403" in content.replace(" ", ""), "abort(403) is missing in app.py."