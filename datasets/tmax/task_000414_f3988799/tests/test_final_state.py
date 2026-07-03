# test_final_state.py

import os
import sqlite3
import pytest

def test_solution_file_correct():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"Solution file {solution_path} does not exist. Did you run the optimizer script?"

    with open(solution_path, 'r') as f:
        content = f.read().strip()

    # Calculate the expected value dynamically based on the DB and correct rate
    db_path = "/home/user/data.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT value FROM metrics WHERE status = 'Active'")
    rows = c.fetchall()
    conn.close()

    val = sum(r[0] for r in rows)
    target = 100.0
    rate = 0.15

    iterations = 0
    while abs(val - target) > 0.1:
        val += (target - val) * rate
        iterations += 1
        if iterations > 1000:
            pytest.fail("Convergence calculation exceeded iteration limit during test verification.")

    expected_val = f"{val:.2f}"

    assert content == expected_val, f"Expected solution '{expected_val}', but got '{content}'. Ensure the convergence logic and database query are correct."

def test_env_file_updated():
    env_path = "/home/user/.env"
    assert os.path.isfile(env_path), f"Environment file {env_path} is missing."

    with open(env_path, 'r') as f:
        content = f.read()

    assert "0.15" in content, "The .env file does not appear to contain the correct CONVERGENCE_RATE extracted from the memory dump."