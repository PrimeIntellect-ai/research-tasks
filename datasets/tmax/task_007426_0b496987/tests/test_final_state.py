# test_final_state.py

import os
import sqlite3
import math
import pytest

def get_expected_yield():
    db_path = '/home/user/analytics/portfolio.db'
    assert os.path.exists(db_path), f"Database missing at {db_path}"

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT t.amount, t.cashflow 
        FROM trades t
        JOIN trade_events e ON t.id = e.trade_id
        WHERE e.status = 'SETTLED'
    """)
    rows = c.fetchall()
    conn.close()

    # Bug 1 fix implies 1000 rows
    assert len(rows) == 1000, "Expected exactly 1000 SETTLED trades from the database."

    # Bug 2 fix implies using math.fsum for precision
    total_val = math.fsum(r[0] for r in rows)

    # Cashflows are just summed
    total_cashflow = sum(r[1] for r in rows)

    # Bug 3 fix implies the yield converges to cashflow / total_val
    expected_yield = total_cashflow / total_val
    return expected_yield

def test_result_file_exists_and_correct():
    result_path = '/home/user/analytics/result.txt'
    assert os.path.exists(result_path), f"The result file was not found at {result_path}. Did the job run successfully?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content, "The result.txt file is empty."

    try:
        actual_yield = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the contents of result.txt as a float. Found: {content}")

    expected_yield = get_expected_yield()
    expected_str = f"{expected_yield:.8f}"

    assert content == expected_str, f"The computed yield in result.txt is incorrect. Expected {expected_str}, but found {content}."

def test_engine_py_fixes():
    engine_path = '/home/user/analytics/engine.py'
    assert os.path.exists(engine_path), f"The file {engine_path} is missing."

    with open(engine_path, 'r') as f:
        code = f.read()

    # Check for evidence of the fixes, without enforcing exact syntax
    assert "SETTLED" in code, "The query does not appear to filter by 'SETTLED' status."
    assert "fsum" in code, "The calculate_total_value function does not appear to use math.fsum."
    assert "==" not in code.split("def calculate_yield")[1], "The calculate_yield function still appears to use exact equality for convergence."