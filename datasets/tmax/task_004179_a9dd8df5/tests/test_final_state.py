# test_final_state.py
import os
import json
import tarfile

def test_fatal_errors_jsonl():
    filepath = "/home/user/fatal_errors.jsonl"
    assert os.path.exists(filepath), f"{filepath} is missing"

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Invalid JSON found in {filepath}: {line}"

    expected_ids = [2, 8, 12, 18]
    actual_ids = [r["id"] for r in records if "id" in r]

    assert actual_ids == expected_ids, f"Expected IDs {expected_ids}, but got {actual_ids}. Ensure records are filtered by FATAL and sorted by id."
    assert all(r.get("level") == "FATAL" for r in records), "Found non-FATAL records in the output."

def test_fatal_backup_tar_gz():
    tar_path = "/home/user/fatal_backup.tar.gz"
    assert os.path.exists(tar_path), f"{tar_path} is missing"

    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive"

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            members = tar.getnames()
            assert "fatal_errors.jsonl" in members, "Archive does not contain 'fatal_errors.jsonl' at the root"

            f = tar.extractfile("fatal_errors.jsonl")
            assert f is not None, "Could not extract 'fatal_errors.jsonl' from the archive"

            content = f.read().decode('utf-8')
            lines = [line.strip() for line in content.splitlines() if line.strip()]

            records = []
            for line in lines:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    assert False, f"Invalid JSON found in archived fatal_errors.jsonl: {line}"

            expected_ids = [2, 8, 12, 18]
            actual_ids = [r["id"] for r in records if "id" in r]

            assert actual_ids == expected_ids, f"Archived file has incorrect IDs. Expected {expected_ids}, got {actual_ids}"
            assert all(r.get("level") == "FATAL" for r in records), "Archived file contains non-FATAL records"
    except tarfile.ReadError:
        assert False, f"{tar_path} is not a valid gzip-compressed tar archive"