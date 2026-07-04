# test_final_state.py
import os
import json
import re

def test_metrics_json_exists_and_valid():
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), f"Missing required file: {metrics_path}"

    with open(metrics_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} is not a valid JSON file"

    assert "mean_distance" in data, f"'mean_distance' key missing in {metrics_path}"

    val = float(data["mean_distance"])
    target = 0.75
    tolerance = 0.15

    assert abs(val - target) <= tolerance, f"mean_distance {val} is not within {tolerance} of target {target}"

def test_audit_log_exists_and_format():
    log_path = "/home/user/audit_log.txt"
    assert os.path.isfile(log_path), f"Missing required file: {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) >= 2, f"{log_path} must contain at least two lines for WORST and BEST"

    worst_found = False
    best_found = False

    for line in lines:
        if line.startswith("WORST:"):
            worst_found = True
            keys = line.replace("WORST:", "").strip().split(",")
            assert len(keys) >= 2, "WORST line must contain at least 2 keys"
        elif line.startswith("BEST:"):
            best_found = True
            keys = line.replace("BEST:", "").strip().split(",")
            assert len(keys) >= 2, "BEST line must contain at least 2 keys"

    assert worst_found, "WORST line missing or incorrectly formatted in audit_log.txt"
    assert best_found, "BEST line missing or incorrectly formatted in audit_log.txt"