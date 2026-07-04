# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

def sanitize_records(records):
    accepted = []
    window = []
    for r in records:
        if r.get("tag") == "ERR_77":
            continue

        current_val = r.get("val", 0)
        current_sum = sum(window) + current_val
        if current_sum > 500:
            continue

        accepted.append(r)
        window.append(current_val)
        if len(window) > 2:
            window.pop(0)

    return accepted

def test_cron_schedule():
    cron_path = "/home/user/pipeline.cron"
    assert os.path.exists(cron_path), f"Cron file missing at {cron_path}"

    with open(cron_path, "r") as f:
        content = f.read().strip()

    valid_expressions = [
        "*/15 * * * 1-5 /home/user/run_pipeline.sh",
        "0,15,30,45 * * * 1-5 /home/user/run_pipeline.sh"
    ]

    # Allow some whitespace variations
    normalized_content = " ".join(content.split())
    assert any(normalized_content.endswith(expr) or expr in normalized_content for expr in valid_expressions), f"Cron expression in {cron_path} does not match expected schedules."

def test_sanitizer_executable():
    bin_path = "/home/user/sanitizer"
    assert os.path.exists(bin_path), f"Sanitizer binary missing at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Sanitizer binary at {bin_path} is not executable"

def test_adversarial_corpus():
    bin_path = "/home/user/sanitizer"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(clean_dir), "Clean corpus directory missing"
    assert os.path.exists(evil_dir), "Evil corpus directory missing"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    clean_modified = []
    evil_bypassed = []

    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "out.json")

        # Test clean corpus
        for f in clean_files:
            in_path = os.path.join(clean_dir, f)
            subprocess.run([bin_path, in_path, out_path], check=True, capture_output=True)

            with open(in_path, "r") as fin:
                in_data = json.load(fin)
            with open(out_path, "r") as fout:
                out_data = json.load(fout)

            if in_data != out_data:
                clean_modified.append(f)

        # Test evil corpus
        for f in evil_files:
            in_path = os.path.join(evil_dir, f)
            subprocess.run([bin_path, in_path, out_path], check=True, capture_output=True)

            with open(in_path, "r") as fin:
                in_data = json.load(fin)
            with open(out_path, "r") as fout:
                out_data = json.load(fout)

            expected_data = sanitize_records(in_data)

            if out_data != expected_data:
                evil_bypassed.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)