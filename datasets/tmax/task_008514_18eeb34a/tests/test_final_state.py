# test_final_state.py

import os
import json
import random
import tarfile
import hashlib
import tempfile
import pytest

def get_expected_data():
    experiments = ["EXP_ALPHA", "EXP_BETA", "EXP_GAMMA"]
    random.seed(42)

    counts = {exp: 0 for exp in experiments}
    corrupted = []

    for i in range(1000):
        if i % 100 == 0:
            corrupted.append(f"CORRUPTED_LINE_{i}{{missing_brackets}}\n")
        else:
            exp = random.choice(experiments)
            counts[exp] += 1
            random.choices(["A", "C", "G", "T"], k=50)

    return counts, corrupted

def test_corrupted_reads_log():
    """Verify that the corrupted reads log contains exactly the expected corrupted lines."""
    log_path = "/home/user/corrupted_reads.log"
    assert os.path.isfile(log_path), f"File not found: {log_path}"

    _, expected_corrupted = get_expected_data()

    with open(log_path, "r") as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_corrupted), f"Expected {len(expected_corrupted)} corrupted lines, found {len(actual_lines)}"
    for expected, actual in zip(expected_corrupted, actual_lines):
        assert expected == actual, f"Mismatch in corrupted log. Expected: {expected.strip()}, Actual: {actual.strip()}"

def test_archives_exist_and_contents():
    """Verify the archives exist and contain the correct number of lines in reads.jsonl."""
    expected_counts, _ = get_expected_data()
    archives_dir = "/home/user/archives"

    for exp, expected_count in expected_counts.items():
        archive_path = os.path.join(archives_dir, f"{exp}_archive.tar.gz")
        assert os.path.isfile(archive_path), f"Archive not found: {archive_path}"

        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getmembers()
            # Find the reads.jsonl file in the archive
            reads_member = None
            for member in members:
                if member.name.endswith("reads.jsonl"):
                    reads_member = member
                    break

            assert reads_member is not None, f"reads.jsonl not found in archive {archive_path}"
            assert not reads_member.name.startswith("/home/"), f"Archive {archive_path} contains absolute paths: {reads_member.name}"

            with tar.extractfile(reads_member) as f:
                lines = f.readlines()
                assert len(lines) == expected_count, f"Expected {expected_count} lines in {exp} archive, found {len(lines)}"

                # Check that lines are valid json and have correct exp id
                for line in lines:
                    record = json.loads(line.decode('utf-8'))
                    assert record["experiment_id"] == exp, f"Found wrong experiment ID in {exp} archive."

def test_final_checksums_txt():
    """Verify the final checksums file contains the correct sha256 sums of the archives."""
    checksums_path = "/home/user/final_checksums.txt"
    assert os.path.isfile(checksums_path), f"File not found: {checksums_path}"

    expected_counts, _ = get_expected_data()
    archives_dir = "/home/user/archives"

    actual_checksums = {}
    for exp in expected_counts.keys():
        archive_path = os.path.join(archives_dir, f"{exp}_archive.tar.gz")
        if os.path.isfile(archive_path):
            hasher = hashlib.sha256()
            with open(archive_path, "rb") as f:
                hasher.update(f.read())
            actual_checksums[f"{exp}_archive.tar.gz"] = hasher.hexdigest()

    with open(checksums_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 3, f"Expected 3 lines in {checksums_path}, found {len(lines)}"

    parsed_checksums = {}
    for line in lines:
        parts = line.split()
        assert len(parts) >= 2, f"Invalid format in checksums file: {line}"
        chksm = parts[0]
        fname = parts[1].lstrip('*./')
        parsed_checksums[os.path.basename(fname)] = chksm

    for exp in expected_counts.keys():
        fname = f"{exp}_archive.tar.gz"
        assert fname in parsed_checksums, f"{fname} missing from {checksums_path}"
        assert parsed_checksums[fname] == actual_checksums.get(fname, ""), f"Checksum mismatch for {fname}"