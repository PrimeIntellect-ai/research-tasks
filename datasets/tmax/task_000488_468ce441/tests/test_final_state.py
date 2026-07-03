# test_final_state.py
import os
import re

def test_fast_processor_exists():
    path = "/home/user/perf_task/fast_processor"
    assert os.path.isfile(path), f"Expected {path} to exist as a file."
    assert os.access(path, os.X_OK), f"Expected {path} to be executable."

def test_unified_timeline_content():
    logs_dir = "/home/user/perf_task/logs"
    timeline_path = "/home/user/perf_task/unified_timeline.log"

    assert os.path.isfile(timeline_path), f"Expected {timeline_path} to exist."

    expected_entries = []
    log_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[([^\]]+)\] val=(\d+)$")

    # Read and parse all original log files
    for filename in os.listdir(logs_dir):
        if filename.endswith(".log"):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    match = log_pattern.match(line)
                    if match:
                        timestamp, service, val_str = match.groups()
                        val = int(val_str)
                        # Recompute the intent (triangular number sequence)
                        metric = (val * (val + 1)) // 2
                        expected_entries.append((timestamp, service, val, metric))

    # Sort chronologically by timestamp
    expected_entries.sort(key=lambda x: x[0])

    expected_lines = [
        f"{ts} | {svc} | {val} | {metric}"
        for ts, svc, val, metric in expected_entries
    ]

    # Read actual output
    with open(timeline_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in unified_timeline.log, "
        f"but got {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch in unified_timeline.log.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )