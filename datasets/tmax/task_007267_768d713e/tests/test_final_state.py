# test_final_state.py

import os
import json

def test_hourly_loc_stats_csv():
    raw_path = "/home/user/raw_edits.jsonl"
    assert os.path.exists(raw_path), f"File {raw_path} is missing."

    events = []
    with open(raw_path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    expected_stats = {}
    hours = ["08", "09", "10", "11", "12"]
    locales = ["de-DE", "es-ES", "fr-FR"]

    for h in hours:
        for l in locales:
            expected_stats[(f"2023-10-01T{h}:00:00Z", l)] = 0

    for ev in events:
        ts = ev["timestamp"]
        # Extract the hour part to form the bucket
        hour_bucket = ts[:11] + ts[11:13] + ":00:00Z"
        loc = ev["locale"]
        eff_words = int(ev["words"] * (ev["tm_match"] / 100))
        if (hour_bucket, loc) in expected_stats:
            expected_stats[(hour_bucket, loc)] += eff_words

    expected_csv_lines = ["timestamp,locale,effective_words"]
    for h in hours:
        for l in locales:
            bucket = f"2023-10-01T{h}:00:00Z"
            expected_csv_lines.append(f"{bucket},{l},{expected_stats[(bucket, l)]}")

    csv_path = "/home/user/hourly_loc_stats.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} is missing."

    with open(csv_path, "r") as f:
        actual_csv_lines = [line.strip() for line in f if line.strip()]

    assert actual_csv_lines == expected_csv_lines, f"CSV content mismatch.\nExpected:\n{expected_csv_lines}\nGot:\n{actual_csv_lines}"

def test_process_log():
    log_path = "/home/user/process.log"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    raw_path = "/home/user/raw_edits.jsonl"
    with open(raw_path, "r") as f:
        num_events = sum(1 for line in f if line.strip())

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "PIPELINE_START" in log_content, "Log file missing PIPELINE_START indicator."
    expected_end_str = f"PIPELINE_END - Processed {num_events} events"
    assert expected_end_str in log_content, f"Log file missing expected end string: '{expected_end_str}'"