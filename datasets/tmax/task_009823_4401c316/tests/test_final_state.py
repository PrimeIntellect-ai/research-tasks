# test_final_state.py

import os
import json
import csv
import re
from datetime import datetime, timedelta
import pytest

RAW_EVENTS_PATH = "/home/user/raw_events.jsonl"
ANONYMIZED_EVENTS_PATH = "/home/user/anonymized_events.jsonl"
EVENT_VOLUME_PATH = "/home/user/event_volume.csv"
LOC_REPORT_PATH = "/home/user/loc_report.html"

@pytest.fixture(scope="module")
def truth_data():
    if not os.path.exists(RAW_EVENTS_PATH):
        pytest.fail(f"Input file {RAW_EVENTS_PATH} is missing.")

    events = []
    with open(RAW_EVENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    if not events:
        pytest.fail("Input file is empty.")

    total_events = len(events)

    minute_counts = {}
    for e in events:
        ts = datetime.strptime(e["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        minute_str = ts.strftime("%Y-%m-%dT%H:%M:00Z")
        minute_counts[minute_str] = minute_counts.get(minute_str, 0) + 1

    minutes_sorted = sorted(minute_counts.keys())
    start_min = datetime.strptime(minutes_sorted[0], "%Y-%m-%dT%H:%M:00Z")
    end_min = datetime.strptime(minutes_sorted[-1], "%Y-%m-%dT%H:%M:00Z")

    expected_csv_rows = []
    current_min = start_min
    zero_minutes = 0
    peak_count = 0

    while current_min <= end_min:
        m_str = current_min.strftime("%Y-%m-%dT%H:%M:00Z")
        count = minute_counts.get(m_str, 0)
        expected_csv_rows.append({"minute": m_str, "event_count": str(count)})
        if count == 0:
            zero_minutes += 1
        if count > peak_count:
            peak_count = count
        current_min += timedelta(minutes=1)

    return {
        "total_events": total_events,
        "expected_csv_rows": expected_csv_rows,
        "zero_minutes": zero_minutes,
        "peak_count": peak_count
    }

def test_anonymized_events_file(truth_data):
    assert os.path.exists(ANONYMIZED_EVENTS_PATH), f"File missing: {ANONYMIZED_EVENTS_PATH}"

    count = 0
    with open(ANONYMIZED_EVENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            count += 1
            data = json.loads(line)

            email = data.get("user_email", "")
            assert email.startswith("***@"), f"Email not anonymized correctly: {email}"

            ip = data.get("ip_address", "")
            assert ip.endswith(".XXX"), f"IP address not anonymized correctly: {ip}"

    assert count == truth_data["total_events"], f"Expected {truth_data['total_events']} anonymized events, found {count}"

def test_event_volume_csv(truth_data):
    assert os.path.exists(EVENT_VOLUME_PATH), f"File missing: {EVENT_VOLUME_PATH}"

    actual_rows = []
    with open(EVENT_VOLUME_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert "minute" in reader.fieldnames and "event_count" in reader.fieldnames, "CSV headers must be 'minute' and 'event_count'"
        for row in reader:
            actual_rows.append(row)

    expected_rows = truth_data["expected_csv_rows"]
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, found {len(actual_rows)}"

    for actual, expected in zip(actual_rows, expected_rows):
        assert actual["minute"] == expected["minute"], f"Expected minute {expected['minute']}, found {actual['minute']}"
        assert actual["event_count"] == expected["event_count"], f"Expected count {expected['event_count']} for minute {expected['minute']}, found {actual['event_count']}"

def test_loc_report_html(truth_data):
    assert os.path.exists(LOC_REPORT_PATH), f"File missing: {LOC_REPORT_PATH}"

    with open(LOC_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    expected_total = f"Total events processed: {truth_data['total_events']}"
    expected_peak = f"Peak events in a single minute: {truth_data['peak_count']}"
    expected_zero = f"Minutes with zero events: {truth_data['zero_minutes']}"

    assert expected_total in content, f"Expected '{expected_total}' in HTML report."
    assert expected_peak in content, f"Expected '{expected_peak}' in HTML report."
    assert expected_zero in content, f"Expected '{expected_zero}' in HTML report."