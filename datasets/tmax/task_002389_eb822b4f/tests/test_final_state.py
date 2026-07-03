# test_final_state.py

import os
import subprocess
import tempfile
import csv
import pytest

EVIL_DIR = "/app/corpus/evil"
CLEAN_DIR = "/app/corpus/clean"
SCRIPT_PATH = "/home/user/etl_pipeline.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    bypassed = []

    for evil_file in evil_files:
        input_path = os.path.join(EVIL_DIR, evil_file)
        with tempfile.NamedTemporaryFile(suffix='.csv') as tmp_out:
            result = subprocess.run(
                ["python", SCRIPT_PATH, "--input", input_path, "--output", tmp_out.name],
                capture_output=True
            )
            if result.returncode != 1:
                bypassed.append(evil_file)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_clean_corpus_accepted_and_sanitized():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    modified = []

    for clean_file in clean_files:
        input_path = os.path.join(CLEAN_DIR, clean_file)
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp_out:
            output_path = tmp_out.name

        try:
            result = subprocess.run(
                ["python", SCRIPT_PATH, "--input", input_path, "--output", output_path],
                capture_output=True
            )
            if result.returncode != 0:
                modified.append(f"{clean_file} (exit code {result.returncode})")
                continue

            if not os.path.isfile(output_path) or os.path.getsize(output_path) == 0:
                modified.append(f"{clean_file} (output file missing or empty)")
                continue

            # Verify clamping logic
            with open(output_path, 'r') as f:
                reader = csv.DictReader(f)
                for row_idx, row in enumerate(reader):
                    try:
                        alpha = float(row.get('Alpha', 0))
                        beta = float(row.get('Beta', 0))
                        gamma = float(row.get('Gamma', 0))

                        if not (-50.0 <= alpha <= 50.0):
                            modified.append(f"{clean_file} (Alpha out of bounds at row {row_idx})")
                            break
                        if not (0.0 <= beta <= 100.0):
                            modified.append(f"{clean_file} (Beta out of bounds at row {row_idx})")
                            break
                        if not (-10.0 <= gamma <= 10.0):
                            modified.append(f"{clean_file} (Gamma out of bounds at row {row_idx})")
                            break
                    except ValueError:
                        modified.append(f"{clean_file} (Non-float value found at row {row_idx})")
                        break
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified or failed: {', '.join(modified)}"