# test_final_state.py
import os
import sqlite3
import pytest

def get_fib_sum(n):
    if n <= 0: return 0
    fibs = [0] * n
    if n > 1:
        fibs[1] = 1
    for i in range(2, n):
        fibs[i] = fibs[i-1] + fibs[i-2]
    return sum(fibs)

def test_fib_ext_c_fixed():
    filepath = "/home/user/project/fib_ext/fib_ext.c"
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    with open(filepath, 'r') as f:
        content = f.read()

    # Check Bug 1 fixed
    assert "i <= n" not in content, "Bug 1 (out-of-bounds write 'i <= n') was not fixed in fib_ext.c"
    # Check Bug 2 fixed
    assert "free(" in content, "Bug 2 (memory leak) was not fixed: missing 'free(...)' in fib_ext.c"

def test_database_schema_and_values():
    db_path = "/home/user/project/data.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist"

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Check table schema
    c.execute("PRAGMA table_info(computations)")
    columns = [row[1] for row in c.fetchall()]
    assert "fib_sum" in columns, "Column 'fib_sum' was not added to computations table"

    # Check data
    c.execute("SELECT n_value, fib_sum FROM computations ORDER BY id")
    rows = c.fetchall()

    for n_value, fib_sum in rows:
        expected_sum = get_fib_sum(n_value)
        assert fib_sum == expected_sum, f"Incorrect fib_sum for n_value={n_value}. Expected {expected_sum}, got {fib_sum}"

    conn.close()

def test_final_sum_txt():
    txt_path = "/home/user/project/final_sum.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist"

    db_path = "/home/user/project/data.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist"

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT n_value FROM computations")
    rows = c.fetchall()
    conn.close()

    expected_total = sum(get_fib_sum(row[0]) for row in rows)

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of {txt_path} is not an integer: {content}"
    assert int(content) == expected_total, f"Incorrect total sum in {txt_path}. Expected {expected_total}, got {content}"