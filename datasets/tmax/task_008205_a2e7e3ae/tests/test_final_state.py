# test_final_state.py

import os
import sqlite3
import pytest

def test_rust_project_exists():
    cargo_toml_path = "/home/user/review_cleaner/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Rust project not found: {cargo_toml_path} is missing."

def test_insert_sql_exists():
    sql_path = "/home/user/insert.sql"
    assert os.path.isfile(sql_path), f"SQL script not found: {sql_path} is missing."
    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read().lower()
        assert "create table" in content, "insert.sql does not contain CREATE TABLE statement."
        assert "insert into" in content, "insert.sql does not contain INSERT INTO statement."

def test_report_md_content():
    report_path = "/home/user/report.md"
    assert os.path.isfile(report_path), f"Report file not found: {report_path} is missing."

    expected_lines = [
        "# Category Report",
        "- apparel: 1 reviews",
        "- books: 1 reviews",
        "- electronics: 2 reviews"
    ]

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Report content does not match expected.\nExpected: {expected_lines}\nActual: {actual_lines}"

def test_sqlite_db_content():
    db_path = "/home/user/reviews.db"
    assert os.path.isfile(db_path), f"SQLite database not found: {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, category, product_name, review_text FROM reviews ORDER BY id ASC")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'reviews' table: {e}")
    finally:
        conn.close()

    assert len(rows) == 4, f"Expected 4 rows in reviews table, found {len(rows)}."

    # Check unescaped content
    db_records = {str(row[0]): row[3] for row in rows}

    assert db_records.get("1") == "Très bien!", f"Record 1 review_text incorrect: {db_records.get('1')}"
    assert db_records.get("2") == "Great—book", f"Record 2 review_text incorrect: {db_records.get('2')}"
    assert db_records.get("3") == "It is ok.", f"Record 3 review_text incorrect: {db_records.get('3')}"
    assert "génial" in db_records.get("4", ""), f"Record 4 review_text incorrect: {db_records.get('4')}"