# test_final_state.py

import os
import json
from collections import defaultdict
import pytest

def test_report_csv_matches_expected():
    """Test that the generated report.csv matches the expected aggregation output."""
    events_path = "/home/user/events.jsonl"
    report_path = "/home/user/report.csv"

    assert os.path.isfile(events_path), f"Input file not found: {events_path}"
    assert os.path.isfile(report_path), f"Output file not found: {report_path}"

    # Recompute the expected output from the events.jsonl file
    stats = defaultdict(lambda: {"count": 0, "sum": 0.0})
    with open(events_path, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Line {i+1} in {events_path} is not valid JSON")

            event_type = ev.get("event_type")
            metadata = ev.get("metadata", {})
            status = metadata.get("status")
            duration = metadata.get("duration")
            user_id = ev.get("user_id")

            if event_type == "query" and status == "success":
                stats[user_id]["count"] += 1
                stats[user_id]["sum"] += duration

    results = []
    for uid, data in stats.items():
        avg = data["sum"] / data["count"]
        results.append((uid, data["count"], avg))

    # Sort by avg_duration_ms DESC, then user_id ASC
    results.sort(key=lambda x: (-x[2], x[0]))

    expected_lines = ["user_id,query_count,avg_duration_ms"]
    for uid, count, avg in results:
        expected_lines.append(f"{uid},{count},{avg:.2f}")

    # Read the actual report.csv
    with open(report_path, 'r') as f:
        actual_content = f.read().strip().split('\n')

    # Compare
    assert len(actual_content) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in report.csv, but found {len(actual_content)}."
    )

    for i, (actual_line, expected_line) in enumerate(zip(actual_content, expected_lines)):
        assert actual_line.strip() == expected_line, (
            f"Mismatch at line {i+1} in report.csv.\n"
            f"Expected: {expected_line}\n"
            f"Found:    {actual_line.strip()}"
        )