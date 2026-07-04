# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def get_expected_data():
    input_path = "/home/user/raw_feedback.jsonl"
    assert os.path.exists(input_path), f"Input file {input_path} is missing."

    valid_records = []
    dropped_count = 0

    with open(input_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)

            # Validation Checkpoint
            if not record.get("timestamp") or not record.get("text") or not record.get("lang"):
                dropped_count += 1
                continue

            # Masking
            if "user_email" in record and record["user_email"]:
                email = record["user_email"]
                if "@" in email:
                    local, domain = email.split("@", 1)
                    if local:
                        record["user_email"] = f"{local[0]}***@{domain}"

            if "ip_address" in record and record["ip_address"]:
                record["ip_address"] = "[IP_REDACTED]"

            valid_records.append(record)

    # Bucketing
    buckets = defaultdict(int)
    for r in valid_records:
        ts = r["timestamp"]
        # e.g., "2023-10-25T14:32:10Z" -> "2023-10-25T14:00:00Z"
        # Since it's ISO8601, we can just slice and replace minutes/seconds
        hour_bucket = ts[:14] + "00:00Z"
        lang = r["lang"]
        buckets[(hour_bucket, lang)] += 1

    return valid_records, dropped_count, buckets

def test_anonymized_feedback():
    expected_records, _, _ = get_expected_data()
    output_path = "/home/user/processed/anonymized_feedback.jsonl"

    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    actual_records = []
    with open(output_path, 'r') as f:
        for line in f:
            if line.strip():
                actual_records.append(json.loads(line))

    assert len(actual_records) == len(expected_records), \
        f"Expected {len(expected_records)} anonymized records, but found {len(actual_records)}."

    expected_dict = {r["id"]: r for r in expected_records}
    actual_dict = {r["id"]: r for r in actual_records}

    for rid, expected_r in expected_dict.items():
        assert rid in actual_dict, f"Record with id {rid} is missing from output."
        actual_r = actual_dict[rid]

        assert actual_r.get("user_email") == expected_r.get("user_email"), \
            f"Email masking failed for id {rid}. Expected {expected_r.get('user_email')}, got {actual_r.get('user_email')}"

        assert actual_r.get("ip_address") == expected_r.get("ip_address"), \
            f"IP masking failed for id {rid}. Expected {expected_r.get('ip_address')}, got {actual_r.get('ip_address')}"

def test_hourly_lang_summary():
    _, _, expected_buckets = get_expected_data()
    output_path = "/home/user/processed/hourly_lang_summary.csv"

    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "CSV file is empty (missing header)."

        # Ensure exact column names, order might vary depending on implementation but spec says exactly three columns
        assert set(header) == {"hour_bucket", "lang", "feedback_count"}, \
            f"CSV header incorrect. Expected {{'hour_bucket', 'lang', 'feedback_count'}}, got {set(header)}"

        hb_idx = header.index("hour_bucket")
        lang_idx = header.index("lang")
        count_idx = header.index("feedback_count")

        actual_buckets = {}
        for row in reader:
            if not row:
                continue
            actual_buckets[(row[hb_idx], row[lang_idx])] = int(row[count_idx])

    assert actual_buckets == expected_buckets, \
        f"Aggregated buckets do not match expected. Expected {expected_buckets}, got {actual_buckets}"

def test_pipeline_logs():
    expected_records, dropped_count, _ = get_expected_data()
    log_path = "/home/user/logs/pipeline.log"

    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        log_content = f.read()

    expected_phrases = [
        "INFO: Pipeline started",
        f"WARNING: Dropped {dropped_count} records due to validation failures",
        f"INFO: Anonymized {len(expected_records)} valid records",
        "INFO: Pipeline complete"
    ]

    for phrase in expected_phrases:
        assert phrase in log_content, f"Expected log phrase '{phrase}' not found in pipeline.log"