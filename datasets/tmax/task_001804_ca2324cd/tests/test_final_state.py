# test_final_state.py

import os
import json
import subprocess
import pytest
import glob

def test_dictdiffer_fixed():
    try:
        import dictdiffer
    except ImportError as e:
        pytest.fail(f"Failed to import dictdiffer. Was it installed and fixed? Error: {e}")

    try:
        diff_result = list(dictdiffer.diff({'a': 1}, {'a': 2}))
        assert len(diff_result) == 1, "dictdiffer.diff did not return expected results."
    except Exception as e:
        pytest.fail(f"dictdiffer.diff failed to run: {e}")

def test_filter_script_corpora():
    filter_script = "/home/user/filter.py"
    assert os.path.exists(filter_script), f"Filter script not found at {filter_script}"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run(["python3", filter_script, cf], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run(["python3", filter_script, ef], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_pipeline_execution_and_log():
    pipeline_script = "/home/user/pipeline.sh"
    assert os.path.exists(pipeline_script), f"Pipeline script not found at {pipeline_script}"
    assert os.access(pipeline_script, os.X_OK), f"Pipeline script {pipeline_script} is not executable."

    # Remove log if exists to start fresh
    log_file = "/home/user/pipeline.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    # Run pipeline
    res = subprocess.run([pipeline_script], capture_output=True, text=True)
    assert res.returncode == 0, f"Pipeline script failed with exit code {res.returncode}. Stderr: {res.stderr}"

    assert os.path.exists(log_file), f"Log file {log_file} was not created."
    with open(log_file, "r") as f:
        actual_log_lines = [line.strip() for line in f if line.strip()]

    # Compute expected log
    incoming_dir = "/app/incoming_configs"
    incoming_files = sorted(glob.glob(os.path.join(incoming_dir, "*.json")))

    baseline_path = "/app/baseline.json"
    with open(baseline_path, "r") as f:
        baseline_data = json.load(f)

    import dictdiffer
    filter_script = "/home/user/filter.py"

    expected_warns = []
    clean_configs = {}

    for inc_file in incoming_files:
        f_res = subprocess.run(["python3", filter_script, inc_file], capture_output=True)
        if f_res.returncode == 1:
            expected_warns.append(f"[WARN] Rejected {inc_file}")
        elif f_res.returncode == 0:
            with open(inc_file, "r") as f:
                data = json.load(f)
            sid = data.get("server_id")
            ts = data.get("timestamp", 0)
            if sid not in clean_configs or ts > clean_configs[sid]["timestamp"]:
                clean_configs[sid] = {"timestamp": ts, "data": data}

    expected_infos = []
    for sid, config in clean_configs.items():
        diffs = list(dictdiffer.diff(baseline_data, config["data"]))
        expected_infos.append(f"[INFO] Processed {sid} with {len(diffs)} changes")

    # We check if all expected warns and infos are in the actual log
    # Since iteration order in bash might vary, we compare sets
    actual_set = set(actual_log_lines)
    expected_set = set(expected_warns + expected_infos)

    missing = expected_set - actual_set
    extra = actual_set - expected_set

    if missing or extra:
        pytest.fail(f"Log contents mismatch.\nMissing expected lines: {missing}\nExtra lines found: {extra}")