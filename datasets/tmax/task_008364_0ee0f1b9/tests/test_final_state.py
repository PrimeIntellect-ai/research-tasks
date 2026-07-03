# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_quarantine_log():
    quarantine_log = "/home/user/quarantine.log"
    assert os.path.exists(quarantine_log), f"{quarantine_log} does not exist."

    with open(quarantine_log, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_quarantined = {"malicious_absolute.tar.gz", "malicious_relative.tar.gz"}
    actual_quarantined = set(lines)

    missing = expected_quarantined - actual_quarantined
    extra = actual_quarantined - expected_quarantined

    assert not missing, f"Missing expected archives in quarantine log: {missing}"
    assert not extra, f"Found extra archives in quarantine log that should be safe: {extra}"

def test_extracted_files_exist():
    # Safe archives extract these files
    expected_files = [
        "/home/user/extracted/safe_bin_alpha",
        "/home/user/extracted/readme.txt",
        "/home/user/extracted/nested/safe_bin_beta"
    ]
    for fpath in expected_files:
        assert os.path.isfile(fpath), f"Expected extracted file {fpath} is missing."

def get_elf_entry_point(filepath):
    # Use readelf to get the entry point
    result = subprocess.run(["readelf", "-h", filepath], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run readelf on {filepath}"

    for line in result.stdout.splitlines():
        if "Entry point address:" in line:
            parts = line.split(":")
            if len(parts) == 2:
                return parts[1].strip()
    return None

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_elf_manifest():
    manifest = "/home/user/elf_manifest.txt"
    assert os.path.exists(manifest), f"{manifest} does not exist."

    # The expected ELFs from the safe archives
    safe_binaries = [
        "/tmp/safe_bin_alpha",
        "/tmp/safe_bin_beta"
    ]

    expected_lines = []
    for bin_path in safe_binaries:
        assert os.path.exists(bin_path), f"Original binary {bin_path} missing from /tmp."
        sha = get_sha256(bin_path)
        base = os.path.basename(bin_path)
        entry = get_elf_entry_point(bin_path)
        assert entry is not None, f"Could not determine entry point for {bin_path}"
        expected_lines.append(f"{sha} {base} {entry}")

    # Sort lines alphabetically by basename (the second field)
    expected_lines.sort(key=lambda x: x.split()[1])

    with open(manifest, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines in manifest, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, \
            f"Line {i+1} mismatch in manifest.\nExpected: {expected}\nActual:   {actual}"