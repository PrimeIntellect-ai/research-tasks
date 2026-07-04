# test_final_state.py

import os
import subprocess
import tempfile
import json
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
SCRIPT_PATH = "/home/user/pipeline.py"

def run_redis_cmd(*args):
    result = subprocess.run(["redis-cli"] + list(args), capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_redis_set_size(key):
    return int(run_redis_cmd("SCARD", key))

def get_redis_list_elements(key):
    out = run_redis_cmd("LRANGE", key, "0", "-1")
    if not out:
        return []
    return out.splitlines()

def test_pipeline_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    if not os.path.isfile(SCRIPT_PATH):
        pytest.fail("Pipeline script is missing.")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.jsonl')]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.jsonl')]

    clean_failed = []
    evil_failed = []

    # Process Clean Corpus
    for filename in clean_files:
        input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(input_path, 'r', encoding='utf-8') as f:
            input_lines = f.readlines()
        input_count = len(input_lines)

        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp_out:
            output_path = tmp_out.name

        # Run script
        res = subprocess.run(["python3", SCRIPT_PATH, "--input", input_path, "--output", output_path], capture_output=True, text=True)
        if res.returncode != 0:
            clean_failed.append(f"{filename} (script crashed)")
            continue

        with open(output_path, 'r', encoding='utf-8') as f:
            output_lines = f.readlines()

        if len(output_lines) != input_count:
            clean_failed.append(f"{filename} (expected {input_count} records, got {len(output_lines)})")
            continue

        # Check normalization (title stripped)
        for line in output_lines:
            try:
                record = json.loads(line)
                if record.get("title") != record.get("title", "").strip():
                    clean_failed.append(f"{filename} (title not stripped)")
                    break
            except Exception:
                clean_failed.append(f"{filename} (invalid JSON output)")
                break

        # Check report
        reports = get_redis_list_elements("processing_reports")
        expected_report = f"Report for {filename}: {input_count} accepted, 0 dropped."
        if expected_report not in reports:
            clean_failed.append(f"{filename} (missing or incorrect report in Redis)")

        os.remove(output_path)

    # Process Evil Corpus
    for filename in evil_files:
        input_path = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(input_path, 'rb') as f:
            input_count = len(f.readlines())

        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp_out:
            output_path = tmp_out.name

        # Run script
        res = subprocess.run(["python3", SCRIPT_PATH, "--input", input_path, "--output", output_path], capture_output=True, text=True)
        if res.returncode != 0:
            evil_failed.append(f"{filename} (script crashed)")
            continue

        with open(output_path, 'r', encoding='utf-8') as f:
            output_lines = f.readlines()

        if len(output_lines) != 0:
            evil_failed.append(f"{filename} (expected 0 records, got {len(output_lines)})")
            continue

        # Check report
        reports = get_redis_list_elements("processing_reports")
        expected_report = f"Report for {filename}: 0 accepted, {input_count} dropped."
        if expected_report not in reports:
            evil_failed.append(f"{filename} (missing or incorrect report in Redis)")

        os.remove(output_path)

    # Summarize results
    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified or failed: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed or failed: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))