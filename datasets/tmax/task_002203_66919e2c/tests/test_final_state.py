# test_final_state.py

import os
import json
import copy
import subprocess
import tempfile
import pytest

def has_pii(obj):
    if isinstance(obj, dict):
        if "ssn" in obj or "email" in obj:
            return True
        return any(has_pii(v) for v in obj.values())
    elif isinstance(obj, list):
        return any(has_pii(v) for v in obj)
    return False

def expected_processing(lines):
    valid_records = []
    for line in lines:
        if not line.strip():
            continue
        record = json.loads(line)
        if not has_pii(record):
            valid_records.append(record)

    result = []
    prev_record = None
    for record in valid_records:
        if prev_record is not None:
            if record["sensor_payload"] == prev_record["sensor_payload"]:
                continue

            gap = record["timestamp"] - prev_record["timestamp"]
            if gap > 1:
                start_val = prev_record["sensor_payload"].get("value", 0.0)
                end_val = record["sensor_payload"].get("value", 0.0)
                for i in range(1, gap):
                    new_record = {
                        "timestamp": prev_record["timestamp"] + i,
                        "sensor_payload": copy.deepcopy(prev_record["sensor_payload"])
                    }
                    new_record["sensor_payload"]["value"] = start_val + (end_val - start_val) * i / gap
                    result.append(new_record)
        result.append(record)
        prev_record = record
    return result

def run_student_script(input_path, output_path):
    script_path = "/home/user/process_series.py"
    assert os.path.isfile(script_path), f"Student script missing at {script_path}"

    # Ensure the student script runs using the current environment
    env = os.environ.copy()
    # Add vendored path to PYTHONPATH to ensure it's picked up if the student relies on it
    env["PYTHONPATH"] = "/app/vendored/jsonlines-3.1.0:" + env.get("PYTHONPATH", "")

    result = subprocess.run(
        ["python3", script_path, input_path, output_path],
        capture_output=True,
        text=True,
        env=env
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, ""

def test_corpora_processing():
    clean_corpus = "/app/corpora/clean"
    evil_corpus = "/app/corpora/evil"

    clean_files = [f for f in os.listdir(clean_corpus) if f.endswith('.jsonl')]
    evil_files = [f for f in os.listdir(evil_corpus) if f.endswith('.jsonl')]

    failed_clean = []
    failed_evil = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for f in clean_files:
            input_path = os.path.join(clean_corpus, f)
            output_path = os.path.join(tmpdir, f"out_clean_{f}")

            with open(input_path, 'r', encoding='utf-8') as infile:
                expected = expected_processing(infile.readlines())

            success, err = run_student_script(input_path, output_path)
            if not success:
                failed_clean.append(f"{f} (crashed: {err.strip()})")
                continue

            if not os.path.isfile(output_path):
                failed_clean.append(f"{f} (no output file)")
                continue

            with open(output_path, 'r', encoding='utf-8') as outfile:
                actual = [json.loads(line) for line in outfile if line.strip()]

            if actual != expected:
                failed_clean.append(f)

        for f in evil_files:
            input_path = os.path.join(evil_corpus, f)
            output_path = os.path.join(tmpdir, f"out_evil_{f}")

            with open(input_path, 'r', encoding='utf-8') as infile:
                expected = expected_processing(infile.readlines())

            success, err = run_student_script(input_path, output_path)
            if not success:
                failed_evil.append(f"{f} (crashed: {err.strip()})")
                continue

            if not os.path.isfile(output_path):
                failed_evil.append(f"{f} (no output file)")
                continue

            with open(output_path, 'r', encoding='utf-8') as outfile:
                actual = [json.loads(line) for line in outfile if line.strip()]

            if actual != expected:
                failed_evil.append(f)

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/failed: {', '.join(failed_clean)}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/failed: {', '.join(failed_evil)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_vendored_library_fixed():
    jsonlines_py = "/app/vendored/jsonlines-3.1.0/jsonlines/jsonlines.py"
    with open(jsonlines_py, "r", encoding="utf-8") as f:
        content = f.read()

    # The perturbation should be commented out or removed
    # If it's still active, the clean files with unicode escapes would have crashed, 
    # but let's do a basic check that the exact active string isn't just sitting there uncommented.
    # A simple check is to ensure that if the string exists, it's preceded by a comment or removed.
    lines = content.split('\n')
    for line in lines:
        if "Unicode escapes strictly forbidden" in line:
            assert line.strip().startswith('#'), "The malicious perturbation in jsonlines.py is not commented out or removed."