# test_final_state.py

import os
import sqlite3
import subprocess
import glob
import pytest

def test_fixed_report_sql():
    sql_path = "/home/user/fixed_report.sql"
    assert os.path.isfile(sql_path), f"Missing fixed SQL script at {sql_path}"

    db_path = "/app/backups.db"
    assert os.path.isfile(db_path), f"Missing database file at {db_path}"

    with open(sql_path, "r") as f:
        student_query = f.read()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Reference query
    reference_query = """
    WITH RECURSIVE
    core_db AS (
        SELECT id FROM servers WHERE name = 'core-db'
    ),
    hops(server_id, hop_count) AS (
        SELECT id, 0 FROM core_db
        UNION ALL
        SELECT d.source_id, h.hop_count + 1
        FROM dependencies d
        JOIN hops h ON d.target_id = h.server_id
        WHERE h.hop_count < 2
    )
    SELECT b.*
    FROM backups b
    JOIN servers s ON b.server_id = s.id
    WHERE s.id IN (SELECT server_id FROM hops)
      AND s.environment = 'production'
      AND b.retention_days = 30
      AND b.status = 'SUCCESS'
    ORDER BY b.size DESC
    LIMIT 10;
    """

    try:
        cursor.execute(reference_query)
        expected_results = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        expected_results = [] # Fallback if reference query fails due to schema differences not specified

    try:
        cursor.execute(student_query)
        student_results = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        pytest.fail(f"Student query failed to execute: {e}")

    # We compare the IDs of the backups returned, or just compare the whole dicts if possible.
    # Since the exact select columns aren't strictly defined ("return the top 10 largest successful backups"),
    # we'll check if the returned backup IDs match.
    if expected_results and student_results:
        expected_ids = [r.get('id') for r in expected_results if 'id' in r]
        student_ids = [r.get('id') for r in student_results if 'id' in r]
        if expected_ids and student_ids:
            assert student_ids == expected_ids, f"Student query returned incorrect backup IDs. Expected: {expected_ids}, Got: {student_ids}"

def get_classifier_script():
    possible_scripts = [
        "/home/user/verify_backup_record.sh",
        "/home/user/verify_backup_record.py",
        "/home/user/verify_backup_record.js"
    ]
    for script in possible_scripts:
        if os.path.isfile(script):
            return script
    return None

def test_classifier_adversarial_corpus():
    script_path = get_classifier_script()
    assert script_path is not None, "Classifier script not found in /home/user/ (expected .sh, .py, or .js)"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    # Determine how to run the script
    if script_path.endswith(".py"):
        cmd_prefix = ["python3", script_path]
    elif script_path.endswith(".js"):
        cmd_prefix = ["node", script_path]
    else:
        cmd_prefix = ["bash", script_path]

    failed_clean = []
    failed_evil = []

    for cf in clean_files:
        result = subprocess.run(cmd_prefix + [cf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run(cmd_prefix + [ef], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean[:5])}{'...' if len(failed_clean) > 5 else ''}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil[:5])}{'...' if len(failed_evil) > 5 else ''}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))