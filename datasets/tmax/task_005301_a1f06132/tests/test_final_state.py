# test_final_state.py

import os
import sys
import json
import subprocess
import tempfile
import csv
import hashlib
import pytest

def test_jsonlines_fix():
    """
    Test that the jsonlines package was fixed and installed,
    and can properly parse unicode escapes.
    """
    try:
        import jsonlines
    except ImportError:
        pytest.fail("jsonlines package is not installed.")

    test_data = '{"key": "value\\u0041"}'
    try:
        reader = jsonlines.Reader([test_data])
        result = next(reader)
        assert result == {"key": "valueA"}, f"Expected {{'key': 'valueA'}}, got {result}"
    except ValueError as e:
        pytest.fail(f"jsonlines failed to parse unicode escape: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when parsing with jsonlines: {e}")

def test_adversarial_corpus_filter():
    """
    Test the filter_configs.py script against the clean and evil corpora.
    Pass requires 100% of evil rejected and 100% of clean preserved.
    """
    script_path = "/home/user/filter_configs.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.jsonl')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.jsonl')]

    evil_bypassed = []
    clean_modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test evil corpus
        for evil_file in evil_files:
            out_file = os.path.join(tmpdir, "evil_out_" + os.path.basename(evil_file))
            subprocess.run([sys.executable, script_path, evil_file, out_file], check=False)

            if os.path.exists(out_file):
                with open(out_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        evil_bypassed.append(os.path.basename(evil_file))

        # Test clean corpus
        for clean_file in clean_files:
            out_file = os.path.join(tmpdir, "clean_out_" + os.path.basename(clean_file))
            subprocess.run([sys.executable, script_path, clean_file, out_file], check=False)

            if not os.path.exists(out_file):
                clean_modified.append(os.path.basename(clean_file))
                continue

            with open(clean_file, 'r') as f1, open(out_file, 'r') as f2:
                orig_lines = f1.readlines()
                new_lines = f2.readlines()
                if orig_lines != new_lines:
                    clean_modified.append(os.path.basename(clean_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail("; ".join(error_msgs))

def compute_expected_metrics(telemetry_file):
    events_per_server = {}
    with open(telemetry_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            server_id = event['server_id']
            if server_id not in events_per_server:
                events_per_server[server_id] = []
            events_per_server[server_id].append(event)

    expected_summary = {}
    for server_id, events in events_per_server.items():
        deduped = []
        last_hash = None
        for event in events:
            config_state = event.get('config_state', {})
            serialized = json.dumps(config_state, sort_keys=True)
            current_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
            if current_hash != last_hash:
                deduped.append(event)
                last_hash = current_hash

        if not deduped:
            continue

        total_dedup = len(deduped)
        max_mem = max(e.get('memory_allocated', 0) for e in deduped)
        expected_summary[server_id] = {
            'total_deduplicated_events': total_dedup,
            'max_memory_allocated': max_mem
        }

    return expected_summary

def test_process_metrics():
    """
    Test the process_metrics.py script output.
    """
    script_path = "/home/user/process_metrics.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    telemetry_file = "/app/eval_data/telemetry.jsonl"

    # Run the script
    subprocess.run([sys.executable, script_path, telemetry_file], check=False)

    summary_file = "/home/user/metrics_summary.csv"
    assert os.path.isfile(summary_file), f"Summary file not found at {summary_file}"

    expected_metrics = compute_expected_metrics(telemetry_file)

    actual_metrics = {}
    with open(summary_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            server_id = row.get('server_id')
            if not server_id:
                continue
            actual_metrics[server_id] = {
                'total_deduplicated_events': int(row['total_deduplicated_events']),
                'max_memory_allocated': int(row['max_memory_allocated'])
            }

    for server_id, expected in expected_metrics.items():
        assert server_id in actual_metrics, f"Missing server_id {server_id} in summary"
        actual = actual_metrics[server_id]
        assert actual['total_deduplicated_events'] == expected['total_deduplicated_events'], \
            f"Server {server_id}: expected {expected['total_deduplicated_events']} deduplicated events, got {actual['total_deduplicated_events']}"
        assert actual['max_memory_allocated'] == expected['max_memory_allocated'], \
            f"Server {server_id}: expected max memory {expected['max_memory_allocated']}, got {actual['max_memory_allocated']}"