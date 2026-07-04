# test_final_state.py
import os
import json
import gzip

def test_script_exists_and_executable():
    path = "/home/user/process_data.sh"
    assert os.path.isfile(path), f"Script {path} does not exist"
    assert os.access(path, os.X_OK), f"Script {path} is not executable"

def test_cleaned_data_jsonl():
    path = "/home/user/cleaned_data.jsonl"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected 3 lines in {path}, found {len(lines)}"

    parsed = []
    for line in lines:
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Line in {path} is not valid JSON: {line}"

    # Check anonymization and redaction
    for record in parsed:
        email = record.get("email")
        if email:
            assert email.startswith("***@"), f"Email not anonymized correctly: {email}"

        message = record.get("message", "")
        assert "\\uZZZZ" not in message, "Found unredacted \\uZZZZ"
        if record.get("event_id") == "e2":
            assert "[REDACTED]" in message, "Message did not contain [REDACTED]"

    # Check deduplication (oldest timestamp)
    e1_records = [r for r in parsed if r["event_id"] == "e1"]
    assert len(e1_records) == 1, "Duplicate e1 found"
    assert e1_records[0]["timestamp"] == "2023-01-01T09:55:00Z", "Did not keep oldest e1"

    e3_records = [r for r in parsed if r["event_id"] == "e3"]
    assert len(e3_records) == 1, "Duplicate e3 found"
    assert e3_records[0]["timestamp"] == "2023-01-01T10:10:00Z", "Did not keep oldest e3"

def test_archive_exists():
    path = "/home/user/archive/cleaned_data.jsonl.gz"
    assert os.path.isfile(path), f"Archive {path} does not exist"

    try:
        with gzip.open(path, 'rt') as f:
            content = f.read()
            assert len(content) > 0, "Gzip file is empty"
    except Exception as e:
        assert False, f"Failed to read gzip file {path}: {e}"

def test_summary_csv():
    path = "/home/user/summary.csv"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 4, f"Expected 4 lines in {path}, found {len(lines)}"
    assert lines[0] == "event_type,count", "Incorrect CSV header"
    assert lines[1] == "click,1", "Incorrect count for click"
    assert lines[2] == "purchase,1", "Incorrect count for purchase"
    assert lines[3] == "view,1", "Incorrect count for view"

def test_pipeline_log():
    path = "/home/user/pipeline.log"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected 3 lines in {path}, found {len(lines)}"
    assert "Total raw lines: 6" in lines[0], "Incorrect total raw lines"
    assert "Valid parsed lines: 5" in lines[1], "Incorrect valid parsed lines"
    assert "Final deduplicated lines: 3" in lines[2], "Incorrect final deduplicated lines"