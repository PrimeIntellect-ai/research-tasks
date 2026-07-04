# test_final_state.py

import os
import re
import json
import csv
import hashlib
import pytest

RAW_LOGS_PATH = "/home/user/raw_logs.txt"
REJECTED_LOGS_PATH = "/home/user/rejected_logs.txt"
CLEAN_EVENTS_PATH = "/home/user/clean_events.jsonl"
STATS_PATH = "/home/user/stats.csv"

def parse_raw_logs():
    if not os.path.exists(RAW_LOGS_PATH):
        return []
    with open(RAW_LOGS_PATH, "r") as f:
        return f.read().strip().split("\n")

def process_logs(raw_lines):
    rejected = []
    clean = []
    seen_hashes = set()

    pattern = re.compile(r"^(.*?)\s*\|\s*(.*?)\s*\|.*Client IP:\s*(.*?),\s*Time taken:\s*(-?\d+)ms,\s*ErrorCode:\s*(.*?)$")
    ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    for line in raw_lines:
        match = pattern.search(line)
        if not match:
            continue

        timestamp, level, ip, duration_str, code = match.groups()
        duration = int(duration_str)

        is_invalid = False
        if duration < 0:
            is_invalid = True
        if not ip_pattern.match(ip):
            is_invalid = True

        if is_invalid:
            rejected.append(line)
            continue

        hash_str = f"{ip}_{code}_{duration}"
        hash_val = hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

        if hash_val not in seen_hashes:
            seen_hashes.add(hash_val)
            clean.append({
                "timestamp": timestamp,
                "level": level,
                "ip": ip,
                "duration": duration,
                "code": code
            })

    return rejected, clean

def compute_stats(clean_events):
    stats = {}
    for ev in clean_events:
        code = ev["code"]
        if code not in stats:
            stats[code] = {"count": 0, "total_duration": 0}
        stats[code]["count"] += 1
        stats[code]["total_duration"] += ev["duration"]

    result = []
    for code in sorted(stats.keys()):
        count = stats[code]["count"]
        avg = stats[code]["total_duration"] / count
        result.append([code, str(count), f"{avg:.2f}"])
    return result

def test_rejected_logs():
    assert os.path.isfile(REJECTED_LOGS_PATH), f"File not found: {REJECTED_LOGS_PATH}"
    raw_lines = parse_raw_logs()
    expected_rejected, _ = process_logs(raw_lines)

    with open(REJECTED_LOGS_PATH, "r") as f:
        actual_rejected = [line.strip() for line in f if line.strip()]

    assert actual_rejected == expected_rejected, "rejected_logs.txt does not contain the correct invalid lines."

def test_clean_events():
    assert os.path.isfile(CLEAN_EVENTS_PATH), f"File not found: {CLEAN_EVENTS_PATH}"
    raw_lines = parse_raw_logs()
    _, expected_clean = process_logs(raw_lines)

    actual_clean = []
    with open(CLEAN_EVENTS_PATH, "r") as f:
        for line in f:
            if line.strip():
                try:
                    actual_clean.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {CLEAN_EVENTS_PATH}: {line}")

    assert len(actual_clean) == len(expected_clean), "clean_events.jsonl has incorrect number of records."
    for actual, expected in zip(actual_clean, expected_clean):
        assert actual == expected, f"Mismatch in clean_events.jsonl. Expected {expected}, got {actual}"

def test_stats_csv():
    assert os.path.isfile(STATS_PATH), f"File not found: {STATS_PATH}"
    raw_lines = parse_raw_logs()
    _, expected_clean = process_logs(raw_lines)
    expected_stats = compute_stats(expected_clean)

    with open(STATS_PATH, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "stats.csv is empty."
    assert rows[0] == ["ErrorCode", "EventCount", "AvgDuration"], "Incorrect header in stats.csv"

    actual_stats = rows[1:]
    assert actual_stats == expected_stats, f"stats.csv data mismatch. Expected {expected_stats}, got {actual_stats}"