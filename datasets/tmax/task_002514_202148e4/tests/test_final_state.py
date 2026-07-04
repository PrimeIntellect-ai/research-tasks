# test_final_state.py

import os
import glob
import subprocess
import pytest

def gap_fill(lines):
    """
    Computes the expected gap-filled output for a given list of CSV lines.
    """
    output = []
    prev_ts = None
    prev_sensor = None
    prev_reading = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(',')
        # If it's a header or malformed, just preserve it
        if len(parts) != 3 or parts[0] == "timestamp_sec":
            output.append(line)
            continue

        try:
            ts = int(parts[0])
        except ValueError:
            output.append(line)
            continue

        sensor = parts[1]
        reading = parts[2]

        if prev_ts is not None and ts > prev_ts + 1:
            for fill_ts in range(prev_ts + 1, ts):
                output.append(f"{fill_ts},{prev_sensor},{prev_reading}")

        output.append(line)
        prev_ts = ts
        prev_sensor = sensor
        prev_reading = reading

    return output

def test_evil_corpus():
    evil_dir = "/opt/verifier/corpora/evil"
    script = "/home/user/filter_and_fill.sh"

    assert os.path.exists(script), f"Sanitizer script not found at {script}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    if not evil_files:
        pytest.skip("No evil CSV files found.")

    bypassed = []
    for f in evil_files:
        res = subprocess.run(["bash", script, f], capture_output=True, text=True)
        # Evil files must be rejected (exit code != 0)
        if res.returncode == 0:
            bypassed.append(os.path.basename(f))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_clean_corpus():
    clean_dir = "/opt/verifier/corpora/clean"
    script = "/home/user/filter_and_fill.sh"

    assert os.path.exists(script), f"Sanitizer script not found at {script}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    if not clean_files:
        pytest.skip("No clean CSV files found.")

    modified = []
    for f in clean_files:
        with open(f, 'r') as infile:
            lines = infile.readlines()

        expected_lines = gap_fill(lines)
        expected_output = "\n".join(expected_lines)

        res = subprocess.run(["bash", script, f], capture_output=True, text=True)

        # Clean files must be accepted (exit code == 0) and stdout must match expected
        if res.returncode != 0:
            modified.append(f"{os.path.basename(f)} (rejected with exit code {res.returncode})")
        elif res.stdout.strip() != expected_output.strip():
            modified.append(f"{os.path.basename(f)} (output mismatch)")

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified or failed: {', '.join(modified)}"

def test_batch_processor_exists():
    batch_script = "/home/user/batch_process.sh"
    assert os.path.exists(batch_script), f"Batch processor script not found at {batch_script}"
    assert os.access(batch_script, os.X_OK) or os.access(batch_script, os.R_OK), f"{batch_script} must be readable/executable"