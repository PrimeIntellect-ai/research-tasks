# test_final_state.py

import os
import csv
import sqlite3
import pytest

def test_top_users_csv():
    csv_path = '/home/user/top_users.csv'
    assert os.path.isfile(csv_path), f"CSV file missing at {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "CSV file is empty or missing header"

        rows = list(reader)
        assert len(rows) > 0, "CSV file contains no data rows"

        # Check specific counts
        user_1_found = False
        user_3_found = False

        for row in rows:
            # Assuming format: user_id, region, msg_count, rank (or similar order, we'll check by ID)
            # The prompt says: "calculate the message volume for each user and rank them within their region"
            # It should have user_id, region, message_count, rank. Let's just look for user_id == '1' and '3'
            # and verify their counts.
            if row[0].strip() == '1':
                user_1_found = True
                assert row[2].strip() == '5', f"User 1 should have 5 messages, found {row[2]}"
            elif row[0].strip() == '3':
                user_3_found = True
                assert row[2].strip() == '4', f"User 3 should have 4 messages, found {row[2]}"

        assert user_1_found, "User 1 not found in top_users.csv"
        assert user_3_found, "User 3 not found in top_users.csv"

def test_shortest_path_txt():
    txt_path = '/home/user/shortest_path.txt'
    assert os.path.isfile(txt_path), f"Shortest path file missing at {txt_path}"

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert content == '1,5,6,3', f"Shortest path incorrect. Expected '1,5,6,3', got '{content}'"

def test_aggregate_sql_fixed():
    sql_path = '/home/user/aggregate.sql'
    assert os.path.isfile(sql_path), f"SQL script missing at {sql_path}"

    with open(sql_path, 'r') as f:
        content = f.read().upper()

    # Check that the implicit cross join was removed
    assert "FROM USERS U, MESSAGES M" not in content, "The aggregate.sql still contains the buggy implicit cross join."

    # Check if a JOIN or correct WHERE clause is used
    has_join = "JOIN" in content
    has_where = "WHERE" in content
    assert has_join or has_where, "The query does not seem to use an explicit JOIN or WHERE clause to fix the cross join."