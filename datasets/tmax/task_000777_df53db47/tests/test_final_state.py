# test_final_state.py
import os
import json
import hashlib

def test_new_config_exists_and_valid():
    new_config_path = '/home/user/new_config.json'
    assert os.path.isfile(new_config_path), f"File not found: {new_config_path}"

    with open(new_config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {new_config_path} is not valid JSON"

    assert "service" in data, "Key 'service' missing in new_config.json"
    assert data["service"] == "db", f"Expected service to be 'db', got {data['service']}"

    assert "recovered_password_length" in data, "Key 'recovered_password_length' missing"
    assert data["recovered_password_length"] == 7, f"Expected recovered_password_length to be 7, got {data['recovered_password_length']}"

    assert "new_hash_algorithm" in data, "Key 'new_hash_algorithm' missing"
    assert data["new_hash_algorithm"] == "sha256", f"Expected new_hash_algorithm to be 'sha256', got {data['new_hash_algorithm']}"

    assert "salt" in data, "Key 'salt' missing"
    salt = data["salt"]
    assert isinstance(salt, str) and len(salt) == 32, "Salt must be a 32-character string"
    try:
        int(salt, 16)
    except ValueError:
        assert False, "Salt must be a valid hex string"

    assert "password_hash" in data, "Key 'password_hash' missing"
    expected_hash = hashlib.sha256((salt + 'hunter2').encode('utf-8')).hexdigest()
    assert data["password_hash"] == expected_hash, f"password_hash does not match expected sha256(salt + password)"

    assert "wordlist_checksum" in data, "Key 'wordlist_checksum' missing"

    wordlist_path = '/home/user/wordlist.txt'
    assert os.path.isfile(wordlist_path), f"Original file {wordlist_path} was deleted or moved"

    with open(wordlist_path, 'rb') as f:
        expected_wordlist_checksum = hashlib.sha256(f.read()).hexdigest()

    assert data["wordlist_checksum"] == expected_wordlist_checksum, "wordlist_checksum does not match the actual SHA256 checksum of wordlist.txt"

def test_original_files_unmodified():
    old_config_path = '/home/user/old_config.json'
    assert os.path.isfile(old_config_path), f"Original file {old_config_path} was deleted or moved"
    with open(old_config_path, 'r') as f:
        data = json.load(f)
    assert data.get("password_hash") == "2ab96390c7dbe3439de74d0c9b0b1767", "old_config.json was modified"