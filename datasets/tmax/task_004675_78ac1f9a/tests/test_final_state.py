# test_final_state.py
import os
import sqlite3
import math

def test_final_report_exists_and_correct():
    report_path = "/home/user/ticket_8492/final_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist. Did you run report.sh and redirect output to it?"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Expected lines based on rounding to 4 decimal places
    expected_user1 = "1,1000000.02,0.0001"

    # User 3 might be formatted as 150.0 or 150.00, variance as 0.0 or 0.0000
    # Let's parse the lines to be robust against minor formatting differences
    parsed_results = {}
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 3, f"Invalid format in final_report.txt: {line}"
        user_id = int(parts[0])
        avg_amt = float(parts[1])
        variance = float(parts[2])
        parsed_results[user_id] = (avg_amt, variance)

    assert 1 in parsed_results, "User 1 is missing from final_report.txt"
    assert math.isclose(parsed_results[1][0], 1000000.02, rel_tol=1e-9), f"User 1 avg_amount incorrect: {parsed_results[1][0]}"
    assert math.isclose(parsed_results[1][1], 0.0001, rel_tol=1e-3, abs_tol=1e-4), f"User 1 variance incorrect in report: {parsed_results[1][1]}"

    assert 3 in parsed_results, "User 3 is missing from final_report.txt"
    assert math.isclose(parsed_results[3][0], 150.0, rel_tol=1e-9), f"User 3 avg_amount incorrect: {parsed_results[3][0]}"
    assert math.isclose(parsed_results[3][1], 0.0, abs_tol=1e-4), f"User 3 variance incorrect in report: {parsed_results[3][1]}"

    assert 2 not in parsed_results, "User 2 should not be in final_report.txt (avg_amount <= 100)"

def test_database_state():
    db_path = "/home/user/ticket_8492/summary.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist. Did you run process.sh?"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, avg_amount, variance FROM user_stats ORDER BY user_id")
    rows = cursor.fetchall()

    assert len(rows) == 3, f"Expected 3 users in the database, found {len(rows)}"

    user_dict = {row[0]: (row[1], row[2]) for row in rows}

    # User 1: 1000000.01, 1000000.02, 1000000.03
    # Mean = 1000000.02
    # Pop Variance = ((0.01)^2 + 0 + (-0.01)^2) / 3 = 0.0002 / 3 ≈ 0.00006666...
    assert 1 in user_dict, "User 1 missing from database"
    assert math.isclose(user_dict[1][0], 1000000.02, rel_tol=1e-9), f"User 1 DB avg_amount incorrect: {user_dict[1][0]}"
    assert math.isclose(user_dict[1][1], 0.00006666666666666667, rel_tol=1e-2, abs_tol=1e-4), f"User 1 DB variance incorrect: {user_dict[1][1]}"

    # User 2: 50.50, 55.50
    # Mean = 53.0
    # Pop Variance = ((-2.5)^2 + (2.5)^2) / 2 = 12.5 / 2 = 6.25
    assert 2 in user_dict, "User 2 missing from database"
    assert math.isclose(user_dict[2][0], 53.0, rel_tol=1e-9), f"User 2 DB avg_amount incorrect: {user_dict[2][0]}"
    assert math.isclose(user_dict[2][1], 6.25, rel_tol=1e-5), f"User 2 DB variance incorrect: {user_dict[2][1]}"

    # User 3: 150.00, 150.00
    # Mean = 150.0
    # Pop Variance = 0.0
    assert 3 in user_dict, "User 3 missing from database"
    assert math.isclose(user_dict[3][0], 150.0, rel_tol=1e-9), f"User 3 DB avg_amount incorrect: {user_dict[3][0]}"
    assert math.isclose(user_dict[3][1], 0.0, abs_tol=1e-9), f"User 3 DB variance incorrect: {user_dict[3][1]}"

    conn.close()