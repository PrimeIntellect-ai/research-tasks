# test_final_state.py

import os
import hashlib

def get_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def test_manifest_exists_and_correct():
    """Verify that manifest.txt is created and contains the correct hashes and paths."""
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    # Compute expected hashes based on the setup script
    hash_safe1 = get_sha256(b"Safe content 1\n")
    hash_safe2 = get_sha256(b"Safe content 2\n")
    hash_nested = get_sha256(b"Nested safe\n")

    expected_lines = [
        f"{hash_nested}  data/nested_safe.txt",
        f"{hash_safe2}  docs/safe2.txt",
        f"{hash_safe1}  safe1.txt"
    ]
    expected_content = "\n".join(expected_lines)

    with open(manifest_path, "r") as f:
        actual_content = f.read().strip()

    # Split into lines and strip whitespace for robust comparison
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Manifest contents are incorrect.\nExpected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_malicious_files_not_extracted():
    """Verify that path traversal attacks were successfully blocked."""
    # Absolute path attack
    assert not os.path.exists("/etc/hacked.txt"), "/etc/hacked.txt was extracted! Absolute path attack succeeded."

    # Traversal attack from main tar
    assert not os.path.exists("/home/hacked2.txt"), "/home/hacked2.txt was extracted! Path traversal attack succeeded."

    # Traversal attack from nested tar
    assert not os.path.exists("/home/user/nested_malicious.txt"), "nested_malicious.txt was extracted outside the extraction dir!"

def test_safe_files_extracted():
    """Verify that the safe files were properly extracted to the target directory."""
    expected_files = [
        "/home/user/extracted/safe1.txt",
        "/home/user/extracted/docs/safe2.txt",
        "/home/user/extracted/data/nested_safe.txt"
    ]

    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected safe file {filepath} was not extracted."

def test_no_malicious_content_in_extracted():
    """Verify that no file containing 'Malicious' exists in the extracted directory."""
    extracted_dir = "/home/user/extracted"
    for root, _, files in os.walk(extracted_dir):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip checking tar files themselves if they were extracted
            if filepath.endswith(".tar"):
                continue
            with open(filepath, "r", errors="ignore") as f:
                content = f.read()
                assert "Malicious!" not in content, f"File {filepath} contains malicious content!"