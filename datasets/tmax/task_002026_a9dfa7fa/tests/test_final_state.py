# test_final_state.py

import os
import csv
import sys
import pytest

APP_DIR = "/home/user/app"
CLEAN_DIR = os.path.join(APP_DIR, "data/clean")
EVIL_DIR = os.path.join(APP_DIR, "data/evil")

sys.path.insert(0, APP_DIR)

def test_env_file_correct():
    env_path = os.path.join(APP_DIR, ".env")
    assert os.path.isfile(env_path), f".env file missing at {env_path}"
    with open(env_path, "r") as f:
        content = f.read()
    assert "REDIS_URL" in content and "6379" in content, "REDIS_URL not correctly set in .env"
    assert "API_PORT=8000" in content.replace(" ", ""), "API_PORT not correctly set in .env"

def test_plot_results_fixed():
    plot_path = os.path.join(APP_DIR, "plot_results.py")
    assert os.path.isfile(plot_path), f"plot_results.py missing at {plot_path}"
    with open(plot_path, "r") as f:
        content = f.read()
    assert "Agg" in content or "agg" in content.lower(), "matplotlib backend 'Agg' not found in plot_results.py"

def test_adversarial_corpus():
    try:
        from detector import classify
    except ImportError as e:
        pytest.fail(f"Could not import classify from detector.py: {e}")

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]

    assert len(evil_files) > 0, "No evil CSV files found."
    assert len(clean_files) > 0, "No clean CSV files found."

    evil_bypassed = []
    clean_modified = []

    for e_file in evil_files:
        with open(os.path.join(EVIL_DIR, e_file), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if classify(row) is not False:
                        evil_bypassed.append(e_file)
                        break
                except Exception:
                    evil_bypassed.append(e_file)
                    break

    for c_file in clean_files:
        with open(os.path.join(CLEAN_DIR, c_file), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if classify(row) is not True:
                        clean_modified.append(c_file)
                        break
                except Exception:
                    clean_modified.append(c_file)
                    break

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:5])}")

    if errors:
        pytest.fail(" | ".join(errors))