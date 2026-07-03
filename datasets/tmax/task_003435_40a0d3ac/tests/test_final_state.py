# test_final_state.py

import os
import json
import re
import subprocess
import tempfile
import pytest

def test_makefile_fixed():
    makefile_path = "/app/vendored/go-rollstat/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-tags=production" in content, "Makefile was not fixed to use '-tags=production'"
    assert "-tags=prod" not in content, "Makefile still contains the faulty '-tags=prod'"

def is_valid_record(record):
    if not isinstance(record.get("ts"), (int, float)) or record["ts"] <= 0:
        return False
    if not isinstance(record.get("val"), (int, float)) or not (-100.0 <= record["val"] <= 100.0):
        return False
    if not isinstance(record.get("id"), str) or not re.match(r"^[A-Z0-9]+$", record["id"]):
        return False
    return True

def compute_expected_output(input_lines):
    records = []
    for line in input_lines:
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
            if is_valid_record(rec):
                records.append(rec)
        except json.JSONDecodeError:
            pass

    if not records:
        return []

    # Sort by ts, keep first occurrence in input order for duplicates
    # Since Python's sort is stable, we can just sort by ts
    # Wait, "keep the one that appears first in the input file"
    # So we should just iterate and keep the first one seen for each ts
    seen_ts = set()
    deduped = []
    for rec in records:
        if rec["ts"] not in seen_ts:
            deduped.append(rec)
            seen_ts.add(rec["ts"])

    deduped.sort(key=lambda x: x["ts"])

    if not deduped:
        return []

    min_ts = deduped[0]["ts"]
    max_ts = deduped[-1]["ts"]

    # Gap fill
    filled = []
    current_idx = 0
    last_valid = None
    for ts in range(min_ts, max_ts + 1):
        if current_idx < len(deduped) and deduped[current_idx]["ts"] == ts:
            last_valid = deduped[current_idx]
            filled.append(last_valid.copy())
            current_idx += 1
        else:
            new_rec = last_valid.copy()
            new_rec["ts"] = ts
            filled.append(new_rec)

    # Rolling average
    output = []
    for i in range(len(filled)):
        window = filled[max(0, i - 2) : i + 1]
        avg = sum(r["val"] for r in window) / len(window)
        rec = filled[i].copy()
        rec["avg"] = round(avg, 2)
        output.append(rec)

    return output

def run_etl(input_path, output_path):
    etl_script = "/home/user/etl.go"
    assert os.path.isfile(etl_script), f"ETL script not found at {etl_script}"

    cmd = ["go", "run", etl_script, input_path, output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"ETL script failed for {input_path}:\n{result.stderr}"

def test_evil_corpus():
    evil_dir = "/app/data/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} not found"

    files = [f for f in os.listdir(evil_dir) if f.endswith(".jsonl")]
    assert len(files) > 0, "No evil corpus files found"

    bypassed = []
    for file in files:
        input_path = os.path.join(evil_dir, file)
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp:
            output_path = tmp.name

        try:
            run_etl(input_path, output_path)

            with open(output_path, "r") as f:
                output_lines = [line.strip() for line in f if line.strip()]

            if len(output_lines) > 0:
                bypassed.append(file)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(files)} evil bypassed: {', '.join(bypassed)}")

def test_clean_corpus():
    clean_dir = "/app/data/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} not found"

    files = [f for f in os.listdir(clean_dir) if f.endswith(".jsonl")]
    assert len(files) > 0, "No clean corpus files found"

    modified = []
    for file in files:
        input_path = os.path.join(clean_dir, file)
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp:
            output_path = tmp.name

        try:
            with open(input_path, "r") as f:
                input_lines = f.readlines()

            expected_output = compute_expected_output(input_lines)

            run_etl(input_path, output_path)

            with open(output_path, "r") as f:
                output_lines = [line.strip() for line in f if line.strip()]

            actual_output = []
            for line in output_lines:
                try:
                    actual_output.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

            if len(actual_output) != len(expected_output):
                modified.append(file)
                continue

            for actual, expected in zip(actual_output, expected_output):
                if actual.get("ts") != expected["ts"] or \
                   actual.get("id") != expected["id"] or \
                   actual.get("val") != expected["val"] or \
                   actual.get("avg") != expected["avg"]:
                    modified.append(file)
                    break
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if modified:
        pytest.fail(f"{len(modified)} of {len(files)} clean modified or incorrectly processed: {', '.join(modified)}")