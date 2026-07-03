# test_final_state.py

import os
import csv
import math
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/sanitize.py"
CLEAN_DIR = "/app/data/clean"
EVIL_DIR = "/app/data/evil"

def run_script(input_csv, output_csv):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, input_csv, output_csv],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_evil_corpus():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert evil_files, "No evil corpus files found."

    bypassed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for evil_file in evil_files:
            out_file = os.path.join(tmpdir, "out.csv")
            res = run_script(evil_file, out_file)

            if res.returncode != 0:
                bypassed_files.append(f"{os.path.basename(evil_file)} (script crashed)")
                continue

            if not os.path.exists(out_file):
                bypassed_files.append(f"{os.path.basename(evil_file)} (no output file)")
                continue

            with open(out_file, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) != 1:
                bypassed_files.append(f"{os.path.basename(evil_file)} (output has {len(rows)-1} data rows, expected 0)")

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"

def test_clean_corpus():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert clean_files, "No clean corpus files found."

    modified_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for clean_file in clean_files:
            out_file = os.path.join(tmpdir, "out.csv")
            res = run_script(clean_file, out_file)

            if res.returncode != 0:
                modified_files.append(f"{os.path.basename(clean_file)} (script crashed)")
                continue

            if not os.path.exists(out_file):
                modified_files.append(f"{os.path.basename(clean_file)} (no output file)")
                continue

            with open(clean_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                original_rows = list(reader)

            # Deduplicate
            seen = set()
            dedup_rows = []
            for row in original_rows:
                key = (row['sensor_id'], row['timestamp'])
                if key not in seen:
                    seen.add(key)
                    dedup_rows.append(row)

            # Compute stats
            pressures = [float(row['pressure_hpa']) for row in dedup_rows]
            n = len(pressures)
            if n > 0:
                mean_p = sum(pressures) / n
                if n > 1:
                    variance = sum((p - mean_p) ** 2 for p in pressures) / (n - 1)
                    std_p = math.sqrt(variance)
                else:
                    std_p = 0.0
            else:
                mean_p = 0.0
                std_p = 0.0

            # Read output
            with open(out_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                out_rows = list(reader)

            if len(out_rows) != len(dedup_rows):
                modified_files.append(f"{os.path.basename(clean_file)} (row count mismatch: {len(out_rows)} vs {len(dedup_rows)})")
                continue

            # Compare
            mismatch = False
            for orig, out in zip(dedup_rows, out_rows):
                # Check original fields
                for k in ['sensor_id', 'timestamp', 'temp_celsius', 'pressure_hpa', 'humidity_pct']:
                    if orig[k] != out[k]:
                        mismatch = True
                        break

                if mismatch:
                    break

                # Check zscore
                p = float(orig['pressure_hpa'])
                expected_z = 0.0 if std_p == 0 else (p - mean_p) / std_p
                expected_z_str = f"{expected_z:.4f}"

                try:
                    out_z = float(out['pressure_zscore'])
                    if abs(out_z - float(expected_z_str)) > 1e-4:
                        mismatch = True
                        break
                except (ValueError, KeyError):
                    mismatch = True
                    break

            if mismatch:
                modified_files.append(f"{os.path.basename(clean_file)} (data mismatch)")

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}"