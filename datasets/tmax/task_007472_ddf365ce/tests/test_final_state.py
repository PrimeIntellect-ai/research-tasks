# test_final_state.py

import os
import json
import csv
import sqlite3

def test_updates_extracted():
    updates_dir = "/home/user/loc_workspace/updates"
    assert os.path.isdir(updates_dir), f"Expected directory {updates_dir} to exist."

    new_strings_path = os.path.join(updates_dir, "new_strings.csv")
    assert os.path.isfile(new_strings_path), f"Expected file {new_strings_path} to exist."

    logs_path = os.path.join(updates_dir, "translation_logs.csv")
    assert os.path.isfile(logs_path), f"Expected file {logs_path} to exist."

def test_fuzzy_matches():
    fuzzy_path = "/home/user/loc_workspace/fuzzy_matches.csv"
    assert os.path.isfile(fuzzy_path), f"Expected file {fuzzy_path} to exist."

    with open(fuzzy_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['new_en_source', 'matched_db_en_source', 'similarity_ratio'], \
            f"Incorrect headers in fuzzy_matches.csv: {reader.fieldnames}"

        rows = list(reader)
        assert len(rows) == 2, f"Expected exactly 2 fuzzy matches, got {len(rows)}."

        # Check specific matches
        r1 = next((r for r in rows if r['new_en_source'] == 'Save changes.'), None)
        assert r1 is not None, "Missing fuzzy match for 'Save changes.'"
        assert r1['matched_db_en_source'] == 'Save changes', "Incorrect DB match for 'Save changes.'"
        assert float(r1['similarity_ratio']) == 0.96, f"Incorrect ratio for 'Save changes.': {r1['similarity_ratio']}"

        r2 = next((r for r in rows if r['new_en_source'] == 'Delete user accounts permanently'), None)
        assert r2 is not None, "Missing fuzzy match for 'Delete user accounts permanently'"
        assert r2['matched_db_en_source'] == 'Delete user account permanently', "Incorrect DB match for 'Delete user accounts permanently'"
        assert float(r2['similarity_ratio']) == 0.984, f"Incorrect ratio for 'Delete user accounts permanently': {r2['similarity_ratio']}"

def test_rolling_stats():
    stats_path = "/home/user/loc_workspace/rolling_stats.csv"
    assert os.path.isfile(stats_path), f"Expected file {stats_path} to exist."

    with open(stats_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['date', 'translator_id', 'rolling_3d_sum'], \
            f"Incorrect headers in rolling_stats.csv: {reader.fieldnames}"

        rows = list(reader)
        assert len(rows) == 6, f"Expected exactly 6 rolling stat rows, got {len(rows)}."

        # Check specific calculations
        u2_10_03 = next((r for r in rows if r['translator_id'] == 'user2' and r['date'] == '2023-10-03'), None)
        assert u2_10_03 is not None, "Missing rolling stat for user2 on 2023-10-03"
        assert int(u2_10_03['rolling_3d_sum']) == 350, f"Incorrect rolling sum for user2 on 2023-10-03: {u2_10_03['rolling_3d_sum']} (expected 350)"

        u1_10_04 = next((r for r in rows if r['translator_id'] == 'user1' and r['date'] == '2023-10-04'), None)
        assert u1_10_04 is not None, "Missing rolling stat for user1 on 2023-10-04"
        assert int(u1_10_04['rolling_3d_sum']) == 900, f"Incorrect rolling sum for user1 on 2023-10-04: {u1_10_04['rolling_3d_sum']} (expected 900)"

def test_final_export_json():
    json_path = "/home/user/loc_workspace/final_export.json"
    assert os.path.isfile(json_path), f"Expected file {json_path} to exist."

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "final_export.json is not valid JSON."

        assert isinstance(data, list), "final_export.json must be a JSON array."
        assert len(data) == 4, f"Expected 4 rows in final DB export, got {len(data)}."

        cancel = next((r for r in data if r.get('en_source') == 'Cancel operation'), None)
        assert cancel is not None, "Missing 'Cancel operation' in final export."
        assert cancel.get('es_target') == 'Cancelar la operación', "Did not update exact match for 'Cancel operation'."

        welcome = next((r for r in data if r.get('en_source') == 'Welcome to the dashboard'), None)
        assert welcome is not None, "Missing 'Welcome to the dashboard' in final export (new string not inserted)."
        assert welcome.get('fr_target') == 'Bienvenue sur le tableau de bord', "Incorrect fr_target for new match."

def test_database_updated():
    db_path = "/home/user/loc_workspace/translations.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM locales;")
    count = cursor.fetchone()[0]
    assert count == 4, f"Expected 4 rows in locales table, found {count}."

    cursor.execute("SELECT es_target FROM locales WHERE en_source='Cancel operation';")
    result = cursor.fetchone()
    assert result is not None, "Row with en_source='Cancel operation' not found in DB."
    assert result[0] == 'Cancelar la operación', "Database was not updated for 'Cancel operation'."

    conn.close()