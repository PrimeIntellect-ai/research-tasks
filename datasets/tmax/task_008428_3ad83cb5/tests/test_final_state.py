# test_final_state.py

import os
import hashlib
import tempfile
import subprocess
import base64

def get_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def test_manifest_correctness():
    """Verify the manifest file is created correctly and contains the right checksums."""
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    expected_files = [
        "/home/user/etc/app/config.yaml",
        "/home/user/etc/db.conf"
    ]

    expected_lines = []
    for filepath in expected_files:
        if os.path.exists(filepath):
            checksum = get_sha256(filepath)
            expected_lines.append(f"{checksum}  {filepath}")

    expected_lines.sort()
    expected_content = "\n".join(expected_lines) + "\n"

    with open(manifest_path, "r") as f:
        actual_content = f.read()

    # Normalize newlines and compare
    assert actual_content.strip() == expected_content.strip(), (
        f"Manifest content is incorrect. Expected:\n{expected_content}\nGot:\n{actual_content}"
    )

def test_backup_cpack_correctness():
    """Verify the backup.cpack file exists, can be decoded, extracted, and contains the correct files."""
    cpack_path = "/home/user/backup.cpack"
    assert os.path.isfile(cpack_path), f"Backup file {cpack_path} is missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Decode base64
        try:
            with open(cpack_path, "r") as f:
                encoded_data = f.read()
            compressed_data = base64.b64decode(encoded_data)
        except Exception as e:
            pytest.fail(f"Failed to base64 decode {cpack_path}: {e}")

        tar_gz_path = os.path.join(tmpdir, "backup.tar.gz")
        with open(tar_gz_path, "wb") as f:
            f.write(compressed_data)

        # Extract tar.gz
        try:
            subprocess.run(["tar", "-xzf", tar_gz_path, "-C", tmpdir], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to extract tar archive from decoded data: {e.stderr.decode()}")

        # Verify extracted files
        expected_extracted_files = [
            "home/user/manifest.txt",
            "home/user/etc/app/config.yaml",
            "home/user/etc/db.conf"
        ]

        for rel_path in expected_extracted_files:
            extracted_path = os.path.join(tmpdir, rel_path)
            assert os.path.isfile(extracted_path), f"Expected file {rel_path} is missing from the extracted archive."

            original_path = "/" + rel_path
            if os.path.exists(original_path):
                # Verify content matches
                assert get_sha256(extracted_path) == get_sha256(original_path), (
                    f"Content of extracted file {rel_path} does not match the original."
                )