# test_final_state.py

import os
import subprocess
import json
import pytest

def test_filter_adversarial_corpus():
    """
    Test the compiled filter against the clean and evil corpora.
    """
    filter_bin = "/app/bin/filter"
    assert os.path.isfile(filter_bin), f"Filter binary not found at {filter_bin}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([filter_bin, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([filter_bin, f], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_messages, " | ".join(error_messages)

def test_timeline_reconstruction():
    """
    Test that the combined timeline is correctly reconstructed.
    """
    timeline_path = "/home/user/timeline.txt"
    assert os.path.isfile(timeline_path), f"Timeline file not found at {timeline_path}"

    # Extract video PTS
    video_path = "/app/debug_run.mp4"
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "frame=pts_time", "-of", "csv=p=0", video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run ffprobe on video"

    pts_list = []
    for line in result.stdout.strip().split('\n'):
        if line:
            try:
                pts_list.append(float(line))
            except ValueError:
                pass

    # Read DB events from WAL
    wal_path = "/app/metadata.wal"
    db_events = []
    if os.path.isfile(wal_path):
        with open(wal_path, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 1)
                if len(parts) == 2:
                    try:
                        db_events.append((float(parts[0]), parts[1]))
                    except ValueError:
                        pass

    # Reconstruct expected timeline
    expected_timeline = []
    for pts in pts_list:
        # Find matching db event within 0.05s
        for db_time, db_desc in db_events:
            if abs(pts - db_time) <= 0.05:
                expected_timeline.append(f"{pts:.6f} - {db_desc}")
                # Assuming one match per frame, break after first match
                break

    # Read actual timeline
    with open(timeline_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    # We check if the actual timeline matches the expected one in terms of matched events
    # The user might format timestamps slightly differently, so we parse them
    actual_parsed = []
    for line in actual_lines:
        parts = line.split(" - ", 1)
        if len(parts) == 2:
            try:
                actual_parsed.append((float(parts[0]), parts[1]))
            except ValueError:
                pass

    expected_parsed = []
    for line in expected_timeline:
        parts = line.split(" - ", 1)
        if len(parts) == 2:
            expected_parsed.append((float(parts[0]), parts[1]))

    assert len(actual_parsed) == len(expected_parsed), f"Expected {len(expected_parsed)} timeline entries, got {len(actual_parsed)}"

    for (act_ts, act_desc), (exp_ts, exp_desc) in zip(actual_parsed, expected_parsed):
        assert abs(act_ts - exp_ts) < 0.001, f"Timestamp mismatch: expected {exp_ts}, got {act_ts}"
        assert act_desc == exp_desc, f"Event description mismatch: expected {exp_desc}, got {act_desc}"

def test_db_parser_compiled():
    """
    Test that the db_parser was compiled successfully.
    """
    parser_bin = "/app/bin/db_parser"
    assert os.path.isfile(parser_bin), f"Database parser binary not found at {parser_bin}"
    assert os.access(parser_bin, os.X_OK), f"Database parser binary is not executable at {parser_bin}"