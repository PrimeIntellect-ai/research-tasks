# test_final_state.py
import os
import gzip
import hashlib

def test_filter_executable():
    assert os.path.exists("/home/user/filter"), "/home/user/filter does not exist"
    assert os.access("/home/user/filter", os.X_OK), "/home/user/filter is not executable"

def test_new_logs_exist():
    assert os.path.isdir("/home/user/new_logs"), "/home/user/new_logs directory is missing"
    assert os.path.isfile("/home/user/new_logs/server1.filtered.log.gz"), "server1.filtered.log.gz is missing"
    assert os.path.isfile("/home/user/new_logs/server2.filtered.log.gz"), "server2.filtered.log.gz is missing"

def test_log_contents():
    log1_path = "/home/user/new_logs/server1.filtered.log.gz"
    log2_path = "/home/user/new_logs/server2.filtered.log.gz"

    try:
        with gzip.open(log1_path, 'rb') as f:
            content1 = f.read().decode('utf-8')
    except Exception as e:
        assert False, f"Failed to read and decode {log1_path} as UTF-8: {e}"

    try:
        with gzip.open(log2_path, 'rb') as f:
            content2 = f.read().decode('utf-8')
    except Exception as e:
        assert False, f"Failed to read and decode {log2_path} as UTF-8: {e}"

    assert "[DEBUG] " not in content1, "server1.filtered.log.gz contains [DEBUG] lines"
    assert "[DEBUG] " not in content2, "server2.filtered.log.gz contains [DEBUG] lines"

    assert "Falla crítica en la conexión" in content1, "server1.filtered.log.gz missing expected UTF-8 content"
    assert "Autenticación fallida para el usuario" in content2, "server2.filtered.log.gz missing expected UTF-8 content"
    assert "Starting server" in content1, "server1.filtered.log.gz missing expected content"
    assert "Cache initialized" in content2, "server2.filtered.log.gz missing expected content"

def test_manifest_sha256():
    manifest_path = "/home/user/manifest.sha256"
    assert os.path.isfile(manifest_path), "/home/user/manifest.sha256 is missing"

    with open(manifest_path, 'r') as f:
        manifest_lines = f.read().strip().split('\n')

    manifest_dict = {}
    for line in manifest_lines:
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            # Handle potential asterisk for binary mode in sha256sum output
            filename = parts[1].strip()
            if filename.startswith('*'):
                filename = filename[1:]
            manifest_dict[filename] = parts[0].strip()

    assert "server1.filtered.log.gz" in manifest_dict, "server1.filtered.log.gz missing from manifest (ensure basenames are used)"
    assert "server2.filtered.log.gz" in manifest_dict, "server2.filtered.log.gz missing from manifest (ensure basenames are used)"

    for filename in ["server1.filtered.log.gz", "server2.filtered.log.gz"]:
        expected_hash = manifest_dict[filename]
        filepath = os.path.join("/home/user/new_logs", filename)
        assert os.path.isfile(filepath), f"File {filename} in manifest does not exist in /home/user/new_logs"
        with open(filepath, 'rb') as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()
        assert actual_hash == expected_hash, f"Hash mismatch for {filename} in manifest"