# test_final_state.py

import os
import json
import glob
import sys
import importlib.util
import pytest

def load_student_module():
    module_path = "/home/user/etl_worker.py"
    assert os.path.isfile(module_path), f"Student script not found at {module_path}"

    spec = importlib.util.spec_from_file_location("etl_worker", module_path)
    etl_worker = importlib.util.module_from_spec(spec)
    sys.modules["etl_worker"] = etl_worker
    try:
        spec.loader.exec_module(etl_worker)
    except Exception as e:
        pytest.fail(f"Failed to execute {module_path}: {e}")

    assert hasattr(etl_worker, "process_payload"), "process_payload function is missing"
    return etl_worker.process_payload

def test_adversarial_evil_corpus():
    process_payload = load_student_module()
    evil_dir = "/app/verifier/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus dir missing: {evil_dir}"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []

    for file_path in evil_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        try:
            result = process_payload(data)
            # Evil corpus records should be completely dropped
            if len(result) > 0:
                bypassed_files.append(os.path.basename(file_path))
        except Exception as e:
            # If it crashes on evil data, that's also a failure to handle it gracefully
            bypassed_files.append(f"{os.path.basename(file_path)} (crashed: {e})")

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")

def test_adversarial_clean_corpus():
    process_payload = load_student_module()
    clean_dir = "/app/verifier/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus dir missing: {clean_dir}"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, "No clean corpus files found."

    modified_files = []

    for file_path in clean_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        try:
            result = process_payload(data)
            # Clean corpus records should be 100% retained
            if len(result) != len(data):
                modified_files.append(os.path.basename(file_path))
                continue

            # Ensure no nulls remain in temperature or humidity
            has_nulls = any(r.get("temperature") is None or r.get("humidity") is None for r in result)
            if has_nulls:
                modified_files.append(f"{os.path.basename(file_path)} (contains nulls)")
                continue

        except Exception as e:
            modified_files.append(f"{os.path.basename(file_path)} (crashed: {e})")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified/dropped. Offending files: {', '.join(modified_files)}")