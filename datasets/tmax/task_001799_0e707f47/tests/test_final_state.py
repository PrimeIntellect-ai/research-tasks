# test_final_state.py

import os
import sqlite3
import subprocess
import pytest
import re

@pytest.fixture(scope="session", autouse=True)
def run_pipeline():
    """Run the pipeline script if it exists and is executable, to ensure artifacts are generated."""
    pipeline_path = '/home/user/pipeline.sh'
    if os.path.isfile(pipeline_path) and os.access(pipeline_path, os.X_OK):
        subprocess.run([pipeline_path], cwd='/home/user', capture_output=True)

def test_pipeline_script_executable():
    pipeline_path = '/home/user/pipeline.sh'
    assert os.path.isfile(pipeline_path), f"{pipeline_path} does not exist"
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable"

def test_html_outputs_exist_and_utf8():
    expected_files = {
        'ja.html': ('こんにちは', '世界'),
        'de.html': ('Grüße', 'Überraschung'),
        'ru.html': ('Привет', 'Мир')
    }

    for filename, (title, content) in expected_files.items():
        filepath = f'/home/user/output/{filename}'
        assert os.path.isfile(filepath), f"Output file {filepath} is missing"

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except UnicodeDecodeError:
            pytest.fail(f"{filepath} is not valid UTF-8")

        assert title in html_content, f"{filepath} does not contain the expected title text '{title}'"
        assert content in html_content, f"{filepath} does not contain the expected content text '{content}'"
        assert "{{TITLE}}" not in html_content, f"{filepath} still contains {{{{TITLE}}}} placeholder"
        assert "{{CONTENT}}" not in html_content, f"{filepath} still contains {{{{CONTENT}}}} placeholder"

def test_database_contents():
    db_path = '/home/user/locales.db'
    assert os.path.isfile(db_path), f"Database {db_path} is missing"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT lang, title_length, content_length FROM metadata ORDER BY lang;")
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query database: {e}")

    expected_rows = [
        ('de', 5, 12),
        ('ja', 5, 2),
        ('ru', 6, 3)
    ]

    assert rows == expected_rows, f"Database contents do not match expected. Got: {rows}"

def test_cron_file():
    cron_path = '/home/user/locales_cron'
    assert os.path.isfile(cron_path), f"Crontab file {cron_path} is missing"

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Look for 0 2 * * * /home/user/pipeline.sh
    # Allow multiple spaces/tabs
    pattern = r'^0\s+2\s+\*\s+\*\s+\*\s+/home/user/pipeline\.sh$'

    match = any(re.match(pattern, line.strip()) for line in content.splitlines() if line.strip())
    assert match, f"Crontab file does not contain the correct schedule for /home/user/pipeline.sh at 2:00 AM"