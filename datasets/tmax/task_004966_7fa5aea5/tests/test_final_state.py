# test_final_state.py

import os
import csv
import sqlite3
import subprocess
import tempfile
import pytest

def get_upper_ratio(text):
    alphas = [c for c in text if c.isalpha()]
    if not alphas:
        return 0.0
    uppers = [c for c in alphas if c.isupper()]
    return len(uppers) / len(alphas)

def test_pipeline_outputs_exist():
    assert os.path.isfile("/home/user/reshaped_long.csv"), "reshaped_long.csv is missing"
    assert os.path.isfile("/home/user/sanitized_long.csv"), "sanitized_long.csv is missing"
    assert os.path.isfile("/home/user/locales.db"), "locales.db is missing"

    templates_dir = "/home/user/templates"
    assert os.path.isdir(templates_dir), "templates directory is missing"

    expected_locales = ["en_US", "fr_FR", "es_ES", "de_DE"]
    for loc in expected_locales:
        po_file = os.path.join(templates_dir, f"locale_{loc}.po")
        assert os.path.isfile(po_file), f"Template file missing: {po_file}"

def test_database_content():
    db_path = "/home/user/locales.db"
    assert os.path.isfile(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translations_ts'")
    assert cursor.fetchone() is not None, "Table translations_ts missing in locales.db"

    cursor.execute("SELECT COUNT(*) FROM translations_ts")
    count = cursor.fetchone()[0]
    assert count > 0, "translations_ts table is empty"
    conn.close()

def test_adversarial_corpus_sanitiser():
    sanitiser_script = "/home/user/sanitiser.py"
    assert os.path.isfile(sanitiser_script), f"Sanitiser script missing: {sanitiser_script}"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    for fname in os.listdir(evil_dir):
        if not fname.endswith(".csv"): continue
        in_path = os.path.join(evil_dir, fname)

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            out_path = tmp.name

        res = subprocess.run(["python3", sanitiser_script, "--input", in_path, "--output", out_path], capture_output=True)
        if res.returncode != 0:
            evil_bypassed.append(f"{fname} (script crashed)")
            continue

        # Check if output dropped the spam rows
        with open(in_path, "r") as f:
            in_rows = list(csv.reader(f))
        with open(out_path, "r") as f:
            out_rows = list(csv.reader(f))

        if len(out_rows) >= len(in_rows):
            evil_bypassed.append(fname)

        os.remove(out_path)

    # Test Clean Corpus
    for fname in os.listdir(clean_dir):
        if not fname.endswith(".csv"): continue
        in_path = os.path.join(clean_dir, fname)

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            out_path = tmp.name

        res = subprocess.run(["python3", sanitiser_script, "--input", in_path, "--output", out_path], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(f"{fname} (script crashed)")
            continue

        with open(in_path, "r") as f:
            in_rows = list(csv.reader(f))
        with open(out_path, "r") as f:
            out_rows = list(csv.reader(f))

        if len(out_rows) != len(in_rows):
            clean_modified.append(fname)

        os.remove(out_path)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(os.listdir(evil_dir))} evil bypassed: " + ", ".join(evil_bypassed))
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(os.listdir(clean_dir))} clean modified: " + ", ".join(clean_modified))

    if errors:
        pytest.fail(" | ".join(errors))