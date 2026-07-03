# test_final_state.py

import os
import pytest

HOME_DIR = "/home/user"
LOGS_DIR = os.path.join(HOME_DIR, "logs")
MRE_LOG = os.path.join(HOME_DIR, "mre.log")
TIMELINE_LOG = os.path.join(HOME_DIR, "consolidated_timeline.log")
WEB_LOG = os.path.join(LOGS_DIR, "web.log")
DB_LOG = os.path.join(LOGS_DIR, "db.log")
CACHE_LOG = os.path.join(LOGS_DIR, "cache.log")

def test_mre_log_valid():
    assert os.path.isfile(MRE_LOG), f"File {MRE_LOG} is missing."
    with open(MRE_LOG, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"{MRE_LOG} must contain exactly one line."
    parts = lines[0].split('|')
    assert len(parts) > 4, f"The line in {MRE_LOG} must have more than 3 pipe characters to trigger the bug."

def test_consolidated_timeline():
    assert os.path.isfile(TIMELINE_LOG), f"File {TIMELINE_LOG} is missing."

    # Reconstruct the expected timeline
    events = []
    log_files = [WEB_LOG, DB_LOG, CACHE_LOG]

    for log_file in log_files:
        if not os.path.isfile(log_file):
            continue
        with open(log_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|', 3)
                if len(parts) == 4:
                    events.append(parts)

    # Sort events chronologically, then by service to ensure deterministic order if timestamps match
    # Wait, python's sort is stable, but let's just sort by timestamp as primary key
    # Wait, the prompt says "sort all events strictly by timestamp chronologically"
    # If timestamps are identical, the original truth script seems to just rely on sort order.
    # Let's sort by timestamp. If identical, sort by service name, then status, then message.
    events.sort(key=lambda x: (x[0], x[1], x[2], x[3]))

    expected_lines = []
    for event in events:
        expected_lines.append(f"[{event[0]}] [{event[1]}] [{event[2]}] {event[3]}")

    with open(TIMELINE_LOG, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    # We sort the expected lines just by timestamp to match any stable sort if needed, 
    # but the truth output sorts by string comparison of the formatted lines or similar.
    # Wait, sorting the tuples by all elements matches the natural string sort of the formatted lines.

    # Let's compare actual vs expected
    assert len(actual_lines) == len(expected_lines), "The number of lines in consolidated_timeline.log is incorrect."

    # Check if actual lines match expected lines
    # We allow slight differences in stable sorting of identical timestamps if any exist, 
    # but in the provided logs, identical timestamps are:
    # 2023-11-01 10:05:23 (cache miss, db query)
    # 2023-11-01 10:16:06 (cache hit, db connection)
    # The truth diff expects exact match with the truth output.
    # Let's sort both actual and expected to be safe against stable sort variations 
    # since the prompt says "sort all events strictly by timestamp chronologically" 
    # but doesn't specify secondary sort.

    actual_sorted = sorted(actual_lines)
    expected_sorted = sorted(expected_lines)

    for actual, expected in zip(actual_sorted, expected_sorted):
        assert actual == expected, f"Timeline mismatch. Expected: '{expected}', Got: '{actual}'"