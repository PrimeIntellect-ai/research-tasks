# test_final_state.py

import os
import sqlite3

def test_solution_file_contains_correct_flag():
    db_path = "/home/user/service/data.db"
    assert os.path.exists(db_path), f"Database file missing at {db_path}"

    # Derive the expected flag directly from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT flag FROM hidden_secrets LIMIT 1")
        row = cursor.fetchone()
    except sqlite3.Error as e:
        assert False, f"Failed to query the database for the expected flag: {e}"
    finally:
        conn.close()

    assert row is not None, "No flag found in the hidden_secrets table."
    expected_flag = row[0]

    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"Solution file not found at {solution_path}"

    with open(solution_path, "r") as f:
        actual_flag = f.read().strip()

    assert actual_flag == expected_flag, f"Solution file contains incorrect flag. Expected '{expected_flag}', got '{actual_flag}'"