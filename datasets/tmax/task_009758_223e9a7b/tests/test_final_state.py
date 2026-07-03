# test_final_state.py
import os
import json
import subprocess
import hashlib

def test_output_file_exists_and_format():
    """Verify that the output file exists and is a valid JSON Lines file."""
    output_file = "/home/user/data/output/clean_feedback.jsonl"
    assert os.path.isfile(output_file), f"Output file {output_file} not found."

    with open(output_file, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 3, f"Expected 3 records in the output file, but got {len(lines)}."

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} is not valid JSON."

        assert "hash" in record, f"Missing 'hash' key in record {i+1}"
        assert "id" in record, f"Missing 'id' key in record {i+1}"
        assert "timestamp" in record, f"Missing 'timestamp' key in record {i+1}"
        assert "normalized_comment" in record, f"Missing 'normalized_comment' key in record {i+1}"

def test_deduplication_and_hashing():
    """Verify that the records are correctly deduplicated, hashed, and earliest timestamp is kept."""
    output_file = "/home/user/data/output/clean_feedback.jsonl"
    if not os.path.isfile(output_file):
        return # Handled by previous test

    records = []
    with open(output_file, 'r') as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    # Expected derived data
    comments = [
        "this is a great product!",
        "terrible, would not buy again.",
        "needs improvement."
    ]

    expected_hashes = {hashlib.sha256(c.encode('utf-8')).hexdigest() for c in comments}

    expected_mapping = {
        hashlib.sha256("this is a great product!".encode('utf-8')).hexdigest(): 201,
        hashlib.sha256("terrible, would not buy again.".encode('utf-8')).hexdigest(): 102,
        hashlib.sha256("needs improvement.".encode('utf-8')).hexdigest(): 202
    }

    found_hashes = set()
    for rec in records:
        h = rec.get("hash")
        found_hashes.add(h)
        assert h in expected_mapping, f"Unexpected hash found: {h} (normalized comment: {rec.get('normalized_comment')})"

        expected_id = expected_mapping[h]
        actual_id = int(rec.get("id"))
        assert actual_id == expected_id, f"For hash {h}, expected ID {expected_id} (earliest timestamp), got {actual_id}."

        # Verify the hash matches the normalized comment
        norm_comment = rec.get("normalized_comment")
        calc_hash = hashlib.sha256(norm_comment.encode('utf-8')).hexdigest()
        assert calc_hash == h, f"Hash {h} does not match SHA-256 of normalized comment '{norm_comment}'"

def test_cron_job_scheduled():
    """Verify that the cron job is scheduled correctly."""
    try:
        cron_out = subprocess.check_output(['crontab', '-l', '-u', 'user'], text=True)
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab for user 'user'."

    lines = cron_out.strip().split('\n')
    found_job = False
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        # Check schedule
        if "0 2 * * *" in line or "00 2 * * *" in line:
            if "process_feedback.py" in line:
                found_job = True
                break

    assert found_job, "Cron job for process_feedback.py at 02:00 AM not found in crontab."