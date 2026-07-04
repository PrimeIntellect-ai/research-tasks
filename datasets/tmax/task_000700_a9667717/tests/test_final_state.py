# test_final_state.py

import os
import sqlite3
import pytest

def test_executable_exists():
    executable_path = "/home/user/project/analyzer"
    assert os.path.isfile(executable_path), "The executable 'analyzer' was not found."
    assert os.access(executable_path, os.X_OK), "The file 'analyzer' is not executable."

def test_config_ini_exists():
    config_path = "/home/user/project/config.ini"
    assert os.path.isfile(config_path), "The file 'config.ini' was not created to prevent the deadlock."

def test_database_recovered():
    db_path = "/home/user/project/sensor_data.db"
    assert os.path.isfile(db_path), "The database file 'sensor_data.db' is missing."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM measurements ORDER BY value ASC;")
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.DatabaseError:
        pytest.fail("The database 'sensor_data.db' is still corrupted or invalid.")
    except sqlite3.OperationalError:
        pytest.fail("The 'measurements' table was not found in the recovered database.")

    values = [row[0] for row in rows]
    expected_values = [10.0, 12.0, 15.0, 18.0, 20.0]
    assert values == expected_values, f"Database values do not match the expected recovered data. Got: {values}"

def test_solution_txt_correct():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), "The file 'solution.txt' was not found."

    with open(solution_path, "r") as f:
        content = f.read().strip()

    expected_content = "Result: 3.6878"
    assert content == expected_content, f"The content of 'solution.txt' is incorrect. Expected '{expected_content}', but got '{content}'."