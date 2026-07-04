# test_final_state.py
import os
import sqlite3

def test_c_program_exists():
    assert os.path.exists("/home/user/reshaper.c"), "/home/user/reshaper.c does not exist"
    assert os.path.exists("/home/user/reshaper"), "/home/user/reshaper (compiled binary) does not exist"
    assert os.access("/home/user/reshaper", os.X_OK), "/home/user/reshaper is not executable"

def test_csv_output_exists():
    assert os.path.exists("/home/user/long_translations.csv"), "/home/user/long_translations.csv does not exist"

def test_sqlite_db_exists_and_schema():
    db_path = "/home/user/translations.db"
    assert os.path.exists(db_path), f"{db_path} does not exist"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='i18n';")
    assert cursor.fetchone() is not None, "Table 'i18n' does not exist in translations.db"

    # Check row counts
    cursor.execute("SELECT COUNT(*) FROM i18n;")
    count = cursor.fetchone()[0]
    # 4 JSON lines * 3 locales (en, fr, ja) = 12
    assert count == 12, f"Expected 12 rows in i18n table, got {count}"

    conn.close()

def test_ja_check_txt():
    txt_path = "/home/user/ja_check.txt"
    assert os.path.exists(txt_path), f"{txt_path} does not exist"

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "farewell|さようなら",
        "greeting|こんにちは",
        "thanks|ありがとう",
        "yes|はい"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {txt_path} do not match the expected output. Got:\n{content}"