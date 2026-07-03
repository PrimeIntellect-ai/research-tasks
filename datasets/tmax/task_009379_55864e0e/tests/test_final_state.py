# test_final_state.py
import os
import tarfile
import tempfile
import hashlib

def test_final_backup_exists():
    assert os.path.exists("/home/user/final_backup.tar.gz"), "The final backup archive /home/user/final_backup.tar.gz does not exist."

def test_final_backup_contents():
    backup_path = "/home/user/final_backup.tar.gz"
    assert os.path.exists(backup_path), "Backup archive missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        # Find the files (they might be in a subdirectory like archive_dir or at the root)
        manifest_path = None
        chunk1_path = None
        chunk2_path = None
        chunk3_path = None

        for root, dirs, files in os.walk(tmpdir):
            if "manifest.txt" in files:
                manifest_path = os.path.join(root, "manifest.txt")
            if "chunk_1.txt" in files:
                chunk1_path = os.path.join(root, "chunk_1.txt")
            if "chunk_2.txt" in files:
                chunk2_path = os.path.join(root, "chunk_2.txt")
            if "chunk_3.txt" in files:
                chunk3_path = os.path.join(root, "chunk_3.txt")

        assert manifest_path is not None, "manifest.txt not found in the archive."
        assert chunk1_path is not None, "chunk_1.txt not found in the archive."
        assert chunk2_path is not None, "chunk_2.txt not found in the archive."
        assert chunk3_path is not None, "chunk_3.txt not found in the archive."

        # Verify line counts
        with open(chunk1_path, "r") as f:
            chunk1_lines = f.readlines()
        assert len(chunk1_lines) == 50, f"Expected chunk_1.txt to have 50 lines, got {len(chunk1_lines)}"

        with open(chunk2_path, "r") as f:
            chunk2_lines = f.readlines()
        assert len(chunk2_lines) == 50, f"Expected chunk_2.txt to have 50 lines, got {len(chunk2_lines)}"

        with open(chunk3_path, "r") as f:
            chunk3_lines = f.readlines()
        assert len(chunk3_lines) == 25, f"Expected chunk_3.txt to have 25 lines, got {len(chunk3_lines)}"

        # Verify md5 checksums in manifest
        def get_md5(filepath):
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()

        expected_md5 = {
            "chunk_1.txt": get_md5(chunk1_path),
            "chunk_2.txt": get_md5(chunk2_path),
            "chunk_3.txt": get_md5(chunk3_path),
        }

        with open(manifest_path, "r") as f:
            manifest_lines = f.read().strip().split('\n')

        manifest_dict = {}
        for line in manifest_lines:
            if not line.strip():
                continue
            parts = line.strip().split()
            assert len(parts) >= 2, f"Invalid manifest line format: {line}"
            # The filename might have a path, so we just check if the chunk name is in the line
            md5_val = parts[0]
            filename = parts[-1]
            manifest_dict[os.path.basename(filename)] = md5_val

        for chunk_name, expected_hash in expected_md5.items():
            assert chunk_name in manifest_dict, f"{chunk_name} missing from manifest.txt"
            assert manifest_dict[chunk_name] == expected_hash, f"MD5 mismatch for {chunk_name}: expected {expected_hash}, got {manifest_dict[chunk_name]}"