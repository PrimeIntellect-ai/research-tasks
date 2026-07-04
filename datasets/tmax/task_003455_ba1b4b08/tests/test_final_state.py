# test_final_state.py
import os
import csv
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/sanitize"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def expected_signature(ts, sid, meas):
    return (ts + (sid * 7) + meas) % 9999

def process_python(input_file):
    # Simulate the expected logic to get the exact output for comparison
    with open(input_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    valid_rows = []
    seen_sigs = set()
    for r in rows:
        ts = int(r["timestamp"])
        sid = int(r["sensor_id"])
        meas = int(r["measurement"])
        sig = int(r["signature"])

        if expected_signature(ts, sid, meas) != sig:
            continue

        if sig in seen_sigs:
            continue
        seen_sigs.add(sig)
        valid_rows.append(r)

    sensor_history = {}
    output_rows = []
    for r in valid_rows:
        sid = int(r["sensor_id"])
        meas = int(r["measurement"])

        if sid not in sensor_history:
            sensor_history[sid] = []
        sensor_history[sid].append(meas)

        window = sensor_history[sid][-3:]
        avg = sum(window) / len(window)

        new_row = dict(r)
        new_row["rolling_avg"] = f"{avg:.2f}"
        output_rows.append(new_row)

    return output_rows

def test_sanitize_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_DIR), f"Clean corpus dir missing: {CLEAN_DIR}"
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith(".csv")]
    assert len(clean_files) > 0, "No clean files found."

    failed_files = []

    for filename in clean_files:
        input_path = os.path.join(CLEAN_DIR, filename)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            output_path = tmp.name

        try:
            result = subprocess.run([SCRIPT_PATH, input_path, output_path], capture_output=True, text=True)
            if result.returncode != 0:
                failed_files.append((filename, f"Exit code {result.returncode} != 0"))
                continue

            if not os.path.isfile(output_path):
                failed_files.append((filename, "Output file not created"))
                continue

            # verify contents
            expected_rows = process_python(input_path)
            with open(output_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                actual_rows = list(reader)

            if len(actual_rows) != len(expected_rows):
                failed_files.append((filename, f"Row count mismatch: expected {len(expected_rows)}, got {len(actual_rows)}"))
                continue

            for i, (exp, act) in enumerate(zip(expected_rows, actual_rows)):
                for k in exp.keys():
                    if exp[k] != act.get(k):
                        failed_files.append((filename, f"Row {i} mismatch on {k}: expected {exp[k]}, got {act.get(k)}"))
                        break
                else:
                    continue
                break

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if failed_files:
        errors = "\n".join([f"{f}: {e}" for f, e in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/failed:\n{errors}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_DIR), f"Evil corpus dir missing: {EVIL_DIR}"
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith(".csv")]
    assert len(evil_files) > 0, "No evil files found."

    bypassed_files = []

    for filename in evil_files:
        input_path = os.path.join(EVIL_DIR, filename)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            output_path = tmp.name

        try:
            result = subprocess.run([SCRIPT_PATH, input_path, output_path], capture_output=True, text=True)
            if result.returncode == 0:
                bypassed_files.append((filename, "Exit code 0 (should be non-zero)"))
                continue

            if os.path.isfile(output_path) and os.path.getsize(output_path) > 0:
                bypassed_files.append((filename, "Output file created and not empty"))
                continue

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if bypassed_files:
        errors = "\n".join([f"{f}: {e}" for f, e in bypassed_files])
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed:\n{errors}")