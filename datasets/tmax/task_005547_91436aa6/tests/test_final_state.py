# test_final_state.py
import os
import json

def test_skipped_logs_file():
    skipped_file = "/home/user/skipped_logs.txt"
    assert os.path.isfile(skipped_file), f"File {skipped_file} does not exist."

    with open(skipped_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_skipped = {
        "/home/user/log_spool/app1/active.txt",
        "/home/user/log_spool/app2/serviceB/active.json"
    }

    assert set(lines) == expected_skipped, f"Expected {expected_skipped} in skipped_logs.txt, got {set(lines)}"
    assert len(lines) == len(expected_skipped), "skipped_logs.txt contains duplicates or extra lines."

def test_archive_jsonl_file():
    archive_file = "/home/user/archive.jsonl"
    assert os.path.isfile(archive_file), f"File {archive_file} does not exist."

    with open(archive_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in archive.jsonl, got {len(lines)}"

    expected_files = {
        "/home/user/log_spool/app1/serviceA/log1.txt",
        "/home/user/log_spool/app1/serviceA/data.csv",
        "/home/user/log_spool/app2/serviceB/event.json",
        "/home/user/log_spool/system.txt"
    }

    found_files = set()
    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line in archive.jsonl is not valid JSON: {line}"

        assert "file" in data, "JSON object missing 'file' key."
        assert "content" in data, "JSON object missing 'content' key."

        found_files.add(data["file"])

        content = data["content"]
        assert ".com" not in content, f"Unredacted '.com' email found in content for {data['file']}"

        if data["file"] != "/home/user/log_spool/system.txt":
            assert "[REDACTED]" in content, f"Expected '[REDACTED]' in content for {data['file']}, but not found."

    assert found_files == expected_files, f"Expected archived files {expected_files}, got {found_files}"