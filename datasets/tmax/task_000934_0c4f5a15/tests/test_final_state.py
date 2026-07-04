# test_final_state.py
import os
import subprocess
import sqlite3
import csv

def test_crontab_entry():
    """Verify that the crontab contains the correct schedule for etl.sh."""
    try:
        # Check crontab for 'user'
        result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
        stdout = result.stdout
    except Exception:
        # Fallback to current user if not running as root or user doesn't exist
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        stdout = result.stdout

    # The cron schedule is every Monday at 3:15 AM
    # "15 3 * * 1 /home/user/etl.sh"
    found = False
    for line in stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            minute, hour, dom, month, dow = parts[:5]
            cmd = " ".join(parts[5:])
            if minute == "15" and hour == "3" and dow == "1" and "/home/user/etl.sh" in cmd:
                found = True
                break

    assert found, "Crontab entry for /home/user/etl.sh at 3:15 AM every Monday is missing or incorrect."

def test_etl_script_executable():
    """Verify that etl.sh exists and is executable."""
    etl_path = "/home/user/etl.sh"
    assert os.path.exists(etl_path), f"{etl_path} does not exist."
    assert os.path.isfile(etl_path), f"{etl_path} is not a file."
    assert os.access(etl_path, os.X_OK), f"{etl_path} is not executable."

def test_pipeline_execution_and_results():
    """Run the ETL script and verify the resulting CSV and SQLite database."""
    # Ensure process.py exists
    assert os.path.exists("/home/user/process.py"), "/home/user/process.py does not exist."

    # Run the ETL script
    result = subprocess.run(["su", "-", "user", "-c", "/home/user/etl.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"etl.sh failed to execute. Output: {result.stderr}"

    csv_path = "/home/user/processed.csv"
    db_path = "/home/user/stats.db"

    assert os.path.exists(csv_path), f"{csv_path} was not created."
    assert os.path.exists(db_path), f"{db_path} was not created."

    # Expected data derived from truth
    expected_data = [
        ("user_alpha", "is", 2),
        ("user_alpha", "ready", 2),
        ("user_alpha", "system", 2),
        ("user_alpha", "booting", 1),
        ("user_alpha", "for", 1),
        ("user_alpha", "processing", 1),
        ("user_alpha", "up", 1),
        ("user_beta", "memory", 2),
        ("user_beta", "warning", 2),
        ("user_beta", "cpu", 1),
        ("user_beta", "freed", 1),
        ("user_beta", "high", 1),
        ("user_beta", "low", 1),
        ("user_gamma", "error", 2),
        ("user_gamma", "404", 1),
        ("user_gamma", "500", 1),
        ("user_gamma", "found", 1),
        ("user_gamma", "not", 1),
    ]

    # Verify CSV contents
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        csv_rows = []
        for row in reader:
            if not row: continue
            assert len(row) == 3, f"CSV row does not have 3 columns: {row}"
            csv_rows.append((row[0], row[1], int(row[2])))

    assert csv_rows == expected_data, f"CSV contents do not match expected sorted data. Got: {csv_rows}"

    # Verify SQLite DB contents
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='word_stats';")
    assert cursor.fetchone() is not None, "Table 'word_stats' does not exist in the database."

    # Check DB rows
    cursor.execute("SELECT user_id, word, frequency FROM word_stats ORDER BY user_id ASC, frequency DESC, word ASC;")
    db_rows = cursor.fetchall()
    conn.close()

    assert db_rows == expected_data, f"Database records do not match expected sorted data. Got: {db_rows}"