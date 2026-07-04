# test_final_state.py

import csv
import io
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

def parse_iso8601(ts):
    # Try parsing standard ISO8601
    try:
        if ts.endswith('Z'):
            ts = ts[:-1] + '+00:00'
        return datetime.fromisoformat(ts)
    except ValueError:
        return ts

def get_expected_output(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Group by user_id
    user_groups = {}
    for row in rows:
        uid = row['user_id']
        if uid not in user_groups:
            user_groups[uid] = []
        user_groups[uid].append(row)

    expected_rows = []
    pattern = re.compile(r'PROJ-XRAY-\d{4}-ZULU')

    for uid, group in user_groups.items():
        # Sort by timestamp chronologically
        group.sort(key=lambda x: parse_iso8601(x['timestamp']))
        first_record = group[0]

        # Check if comments contain the pattern
        if pattern.search(first_record['comments']):
            continue

        # Strip whitespace from comments
        first_record['comments'] = first_record['comments'].strip()
        expected_rows.append(first_record)

    return expected_rows

def run_rust_tool(csv_path):
    manifest_path = "/home/user/filter_project/Cargo.toml"
    assert os.path.exists(manifest_path), f"Rust project not found at {manifest_path}"

    cmd = ["cargo", "run", "--manifest-path", manifest_path, "--", str(csv_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Cargo run failed for {csv_path}:\n{result.stderr}")

    output = result.stdout.strip()
    if not output:
        return []

    reader = csv.DictReader(io.StringIO(output))
    return list(reader)

def test_clean_corpus():
    clean_dir = Path("/app/corpora/clean")
    assert clean_dir.exists() and clean_dir.is_dir()

    failed_files = []

    for csv_file in clean_dir.glob("*.csv"):
        expected = get_expected_output(csv_file)
        try:
            actual = run_rust_tool(csv_file)
        except Exception as e:
            failed_files.append(f"{csv_file.name} (Execution failed: {e})")
            continue

        # Compare sets of tuples to ignore output ordering
        expected_set = {tuple(row.items()) for row in expected}
        actual_set = {tuple(row.items()) for row in actual}

        if expected_set != actual_set:
            failed_files.append(csv_file.name)

    assert not failed_files, f"{len(failed_files)} clean corpus files failed or modified incorrectly: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_dir = Path("/app/corpora/evil")
    assert evil_dir.exists() and evil_dir.is_dir()

    failed_files = []

    for csv_file in evil_dir.glob("*.csv"):
        expected = get_expected_output(csv_file)
        # Evil corpus should result in empty output (or just headers)
        try:
            actual = run_rust_tool(csv_file)
        except Exception as e:
            failed_files.append(f"{csv_file.name} (Execution failed: {e})")
            continue

        expected_set = {tuple(row.items()) for row in expected}
        actual_set = {tuple(row.items()) for row in actual}

        if expected_set != actual_set:
            failed_files.append(csv_file.name)

    assert not failed_files, f"{len(failed_files)} evil corpus files bypassed sanitization: {', '.join(failed_files)}"