# test_final_state.py

import os
import json
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/analyze_pipelines.py"

def run_script(input_file, output_file):
    if not os.path.exists(SCRIPT_PATH):
        return False, "Script not found"

    try:
        subprocess.run(
            ["python3", SCRIPT_PATH, input_file, output_file],
            check=True,
            capture_output=True,
            text=True
        )
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, f"Script failed: {e.stderr}"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"{SCRIPT_PATH} is missing."

def test_evil_corpus():
    evil_files = glob.glob("/app/corpus/evil/*.json")
    assert evil_files, "Evil corpus is missing or empty."

    bypassed = []
    for evil_file in evil_files:
        output_file = evil_file + ".out"
        success, err = run_script(evil_file, output_file)
        if not success:
            bypassed.append(f"{os.path.basename(evil_file)} (Execution failed: {err})")
            continue

        try:
            with open(output_file, 'r') as f:
                output_data = json.load(f)
            if output_data != []:
                bypassed.append(os.path.basename(evil_file))
        except Exception:
            bypassed.append(f"{os.path.basename(evil_file)} (Invalid JSON output)")

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_clean_corpus():
    clean_files = glob.glob("/app/corpus/clean/*.json")
    assert clean_files, "Clean corpus is missing or empty."

    modified = []
    for clean_file in clean_files:
        output_file = clean_file + ".out"
        success, err = run_script(clean_file, output_file)
        if not success:
            modified.append(f"{os.path.basename(clean_file)} (Execution failed: {err})")
            continue

        try:
            with open(clean_file, 'r') as f:
                input_data = json.load(f)
            with open(output_file, 'r') as f:
                output_data = json.load(f)
            if output_data != input_data:
                modified.append(os.path.basename(clean_file))
        except Exception:
            modified.append(f"{os.path.basename(clean_file)} (Invalid JSON output)")

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified: {', '.join(modified)}"