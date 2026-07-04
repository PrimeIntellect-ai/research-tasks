# test_final_state.py

import os
import json
from datetime import datetime, timedelta
from collections import Counter

def test_processed_logs_metric():
    raw_logs_path = "/home/user/raw_logs.jsonl"
    processed_logs_path = "/home/user/processed_logs.jsonl"

    assert os.path.exists(raw_logs_path), f"Raw logs missing at {raw_logs_path}"
    assert os.path.exists(processed_logs_path), f"Processed logs missing at {processed_logs_path}"

    # 1. Read raw logs to get ground truth data
    raw_data = {}
    raw_lang_counts = Counter()
    total_raw = 0

    with open(raw_logs_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            rec_id = record["id"]
            lang = record["lang"]
            msg = record["msg"]

            # Expected timestamp
            dt = datetime(2023, 1, 1) + timedelta(minutes=rec_id)
            expected_ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Expected tokens (strtok in C skips consecutive spaces)
            expected_tokens = [t.lower() for t in msg.split() if t.strip()]

            raw_data[rec_id] = {
                "lang": lang,
                "expected_ts": expected_ts,
                "expected_tokens": expected_tokens
            }
            raw_lang_counts[lang] += 1
            total_raw += 1

    raw_props = {k: v / total_raw for k, v in raw_lang_counts.items()}

    # 2. Read processed logs
    processed_records = []
    with open(processed_logs_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            processed_records.append(json.loads(line))

    assert len(processed_records) == 1000, f"Expected exactly 1000 records in processed logs, got {len(processed_records)}"

    # 3. Check language distribution
    proc_lang_counts = Counter(r.get("lang") for r in processed_records)
    total_proc = len(processed_records)
    proc_props = {k: v / total_proc for k, v in proc_lang_counts.items()}

    all_langs = set(raw_props.keys()).union(set(proc_props.keys()))
    max_diff = 0.0
    for lang in all_langs:
        diff = abs(raw_props.get(lang, 0.0) - proc_props.get(lang, 0.0))
        if diff > max_diff:
            max_diff = diff

    assert max_diff < 0.02, f"Language distribution mismatch. Max absolute difference is {max_diff:.4f}, which is >= 0.02. Raw: {raw_props}, Processed: {proc_props}"

    # 4. Calculate Valid Sample Proportion
    valid_count = 0
    for rec in processed_records:
        rec_id = rec.get("id")
        if rec_id not in raw_data:
            continue

        expected = raw_data[rec_id]

        # Check schema and values
        if rec.get("timestamp") != expected["expected_ts"]:
            continue
        if rec.get("lang") != expected["lang"]:
            continue
        if rec.get("tokens") != expected["expected_tokens"]:
            continue

        valid_count += 1

    valid_proportion = valid_count / total_proc

    assert valid_proportion >= 0.95, f"Valid Sample Proportion is {valid_proportion:.4f}, which is below the threshold of 0.95. {valid_count} out of {total_proc} records were perfectly processed."