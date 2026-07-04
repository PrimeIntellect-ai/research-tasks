# test_final_state.py

import os
import subprocess
import json
import pytest

BINARY_PATH = "/app/vendored/telemetry-processor/target/release/telemetry-processor"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Did you run `make build` successfully?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def run_binary_on_file(filepath):
    try:
        result = subprocess.run(
            [BINARY_PATH, filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else [], result.returncode
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution timed out for {filepath}")
    except Exception as e:
        pytest.fail(f"Execution failed for {filepath}: {e}")

def compute_expected_clean(lines):
    # Recompute the expected output for clean records
    expected = []
    history = {}
    last_accepted = {}

    for line in lines:
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        sensor_id = record.get("sensor_id")
        value = record.get("value")
        message = record.get("message")

        # Deduplication
        if sensor_id in last_accepted:
            if last_accepted[sensor_id] == message:
                continue

        last_accepted[sensor_id] = message

        if sensor_id not in history:
            history[sensor_id] = []
        history[sensor_id].append(value)

        recent = history[sensor_id][-3:]
        rolling_avg = sum(recent) / len(recent)

        out_record = record.copy()
        out_record["rolling_avg"] = rolling_avg
        expected.append(out_record)

    return expected

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.fail(f"Clean corpus directory missing: {CLEAN_CORPUS_DIR}")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".jsonl")]
    modified_files = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        expected_records = compute_expected_clean(raw_lines)
        output_lines, _ = run_binary_on_file(filepath)

        output_records = []
        for line in output_lines:
            try:
                output_records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

        if len(output_records) != len(expected_records):
            modified_files.append(filename)
            continue

        for exp, out in zip(expected_records, output_records):
            if exp.get("sensor_id") != out.get("sensor_id") or exp.get("message") != out.get("message"):
                modified_files.append(filename)
                break
            if abs(exp.get("rolling_avg", 0) - out.get("rolling_avg", -1)) > 1e-5:
                modified_files.append(filename)
                break

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}")

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.fail(f"Evil corpus directory missing: {EVIL_CORPUS_DIR}")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".jsonl")]
    bypassed_files = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        output_lines, _ = run_binary_on_file(filepath)

        if output_lines and len(output_lines) > 0:
            bypassed_files.append(filename)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")