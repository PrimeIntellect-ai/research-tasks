# test_final_state.py
import os
import json
import csv
import unicodedata
from datetime import datetime, timedelta

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Pipeline script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Pipeline script {script_path} is not executable"

def test_crontab_file_exists_and_correct():
    cron_path = "/home/user/my_cron"
    assert os.path.exists(cron_path), f"Crontab file not found at {cron_path}"

    with open(cron_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    assert len(lines) >= 1, f"No valid cron jobs found in {cron_path}"

    found_valid_cron = False
    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            # Check schedule: 0 * * * *
            if parts[0] == "0" and parts[1] == "*" and parts[2] == "*" and parts[3] == "*" and parts[4] == "*":
                # Check command contains pipeline.sh
                if "/home/user/pipeline.sh" in line:
                    found_valid_cron = True
                    break

    assert found_valid_cron, f"Could not find a valid hourly cron job for pipeline.sh in {cron_path}. Found lines: {lines}"

def test_hourly_summary_csv():
    csv_path = "/home/user/hourly_summary.csv"
    assert os.path.exists(csv_path), f"Output CSV not found at {csv_path}"

    raw_logs_path = "/home/user/raw_logs.jsonl"
    assert os.path.exists(raw_logs_path), f"Raw logs file missing at {raw_logs_path}"

    # Recompute expected results
    logs = []
    last_time = None
    with open(raw_logs_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)

            # Forward fill time
            if data.get("time"):
                last_time = data["time"]

            # Parse time
            dt = datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%SZ")
            hour_bin = dt.replace(minute=0, second=0, microsecond=0)

            # Normalize query and get length
            query = data.get("query", "")
            norm_query = unicodedata.normalize("NFKC", query)
            q_len = len(norm_query)

            # Determine if bot
            ua = data.get("ua", "")
            is_bot = 1 if "bot" in ua.lower() else 0

            logs.append({
                "hour": hour_bin,
                "q_len": q_len,
                "is_bot": is_bot
            })

    if not logs:
        return # nothing to test

    min_hour = min(log["hour"] for log in logs)
    max_hour = max(log["hour"] for log in logs)

    # Aggregate
    expected_data = {}
    curr_hour = min_hour
    while curr_hour <= max_hour:
        expected_data[curr_hour] = {"total": 0, "bots": 0, "q_lens": []}
        curr_hour += timedelta(hours=1)

    for log in logs:
        h = log["hour"]
        expected_data[h]["total"] += 1
        expected_data[h]["bots"] += log["is_bot"]
        expected_data[h]["q_lens"].append(log["q_len"])

    expected_rows = []
    curr_hour = min_hour
    while curr_hour <= max_hour:
        stats = expected_data[curr_hour]
        total = stats["total"]
        bots = stats["bots"]
        if total > 0:
            avg_len = sum(stats["q_lens"]) / total
        else:
            avg_len = 0.0

        expected_rows.append({
            "hour": curr_hour.strftime("%Y-%m-%d %H:00:00"),
            "total_requests": str(total),
            "bot_requests": str(bots),
            "avg_query_length": f"{avg_len:.2f}".rstrip('0').rstrip('.') if avg_len == 0.0 else str(round(avg_len, 2))
        })
        curr_hour += timedelta(hours=1)

    # Read actual CSV
    actual_rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["hour", "total_requests", "bot_requests", "avg_query_length"], \
            f"CSV headers are incorrect. Expected ['hour', 'total_requests', 'bot_requests', 'avg_query_length'], got {reader.fieldnames}"
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in CSV, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual["hour"] == expected["hour"], f"Row {i+1} hour mismatch: expected {expected['hour']}, got {actual['hour']}"
        assert actual["total_requests"] == expected["total_requests"], f"Row {i+1} total_requests mismatch: expected {expected['total_requests']}, got {actual['total_requests']}"
        assert actual["bot_requests"] == expected["bot_requests"], f"Row {i+1} bot_requests mismatch: expected {expected['bot_requests']}, got {actual['bot_requests']}"

        # Float comparison for average length
        actual_avg = float(actual["avg_query_length"])
        expected_avg = float(expected["avg_query_length"])
        assert abs(actual_avg - expected_avg) < 0.011, \
            f"Row {i+1} avg_query_length mismatch: expected {expected_avg}, got {actual_avg}"