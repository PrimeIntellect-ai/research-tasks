# test_final_state.py

import os
import json
import sqlite3
import csv
import difflib
import pytest

DB_PATH = "/home/user/etl_results.db"
JSON_PATH = "/home/user/summary.json"
RAW_DATA_PATH = "/home/user/raw_products.csv"

def test_db_exists():
    """Check if the ETL results database exists."""
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}"

def test_json_exists():
    """Check if the summary JSON exists."""
    assert os.path.exists(JSON_PATH), f"Summary JSON not found at {JSON_PATH}"

def test_long_products_table():
    """Verify the long_products table structure and row count."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='long_products'")
    assert c.fetchone() is not None, "Table 'long_products' does not exist in the database."

    c.execute("SELECT COUNT(*) FROM long_products")
    long_count = c.fetchone()[0]
    assert long_count == 300, f"Expected 300 long products, got {long_count}"
    conn.close()

def test_similar_pairs_table_and_json():
    """Verify the similar_pairs table exists and matches the JSON summary."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='similar_pairs'")
    assert c.fetchone() is not None, "Table 'similar_pairs' does not exist in the database."

    with open(JSON_PATH, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Summary JSON is not valid JSON.")

    for lang in ['en', 'fr', 'es']:
        c.execute("SELECT COUNT(*) FROM similar_pairs WHERE language=?", (lang,))
        db_count = c.fetchone()[0]
        json_count = summary.get(lang)
        assert json_count is not None, f"Language '{lang}' missing from JSON summary."
        assert json_count == db_count, f"Mismatch in {lang} pairs: JSON says {json_count}, DB says {db_count}"

    conn.close()

def test_similar_pairs_correctness():
    """Recompute the similarity pairs from the raw data and verify the database contains the exact correct pairs."""
    assert os.path.exists(RAW_DATA_PATH), f"Raw data file not found at {RAW_DATA_PATH}"

    products = {'en': [], 'fr': [], 'es': []}
    with open(RAW_DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('name_en'): products['en'].append((row['vendor_id'], row['name_en']))
            if row.get('name_fr'): products['fr'].append((row['vendor_id'], row['name_fr']))
            if row.get('name_es'): products['es'].append((row['vendor_id'], row['name_es']))

    expected_pairs = {'en': set(), 'fr': set(), 'es': set()}
    for lang in ['en', 'fr', 'es']:
        items = products[lang]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                v1, n1 = items[i]
                v2, n2 = items[j]
                if v1 > v2:
                    v1, v2 = v2, v1
                    n1, n2 = n2, n1
                ratio = difflib.SequenceMatcher(None, n1, n2).ratio()
                if ratio >= 0.85:
                    expected_pairs[lang].add((v1, v2))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for lang in ['en', 'fr', 'es']:
        c.execute("SELECT vendor_id_1, vendor_id_2 FROM similar_pairs WHERE language=?", (lang,))
        db_pairs = set()
        for row in c.fetchall():
            v1, v2 = row[0], row[1]
            if v1 > v2:
                v1, v2 = v2, v1
            db_pairs.add((v1, v2))

        assert db_pairs == expected_pairs[lang], (
            f"Mismatch in similar pairs for language '{lang}'. "
            f"Expected {len(expected_pairs[lang])} pairs, got {len(db_pairs)} pairs. "
            f"Expected pairs: {expected_pairs[lang]}, DB pairs: {db_pairs}"
        )
    conn.close()