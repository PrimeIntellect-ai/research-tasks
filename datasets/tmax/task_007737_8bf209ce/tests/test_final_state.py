# test_final_state.py

import os
import csv
import sqlite3
import pytest
from collections import defaultdict

def test_analyze_script_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_finance_db_exists_and_index():
    db_path = "/home/user/finance.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    # Check if index exists
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_src_date'")
    row = cursor.fetchone()
    conn.close()
    assert row is not None, "Index 'idx_src_date' was not created in the database."

def test_alerts_csv_content():
    accounts_path = "/home/user/accounts.csv"
    transactions_path = "/home/user/transactions.csv"
    alerts_path = "/home/user/alerts.csv"

    assert os.path.isfile(alerts_path), f"Output file {alerts_path} does not exist."

    # Compute expected results
    accounts = {}
    with open(accounts_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            accounts[row["account_id"]] = row["account_name"]

    transactions = defaultdict(list)
    with open(transactions_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions[row["src_id"]].append({
                "amount": float(row["amount"]),
                "tx_date": row["tx_date"]
            })

    expected_alerts = []
    for src_id, txs in transactions.items():
        # sort by date ascending
        txs.sort(key=lambda x: x["tx_date"])
        running_total = 0.0
        for tx in txs:
            running_total += tx["amount"]
            if running_total > 5000:
                expected_alerts.append({
                    "account_name": accounts[src_id],
                    "tx_date": tx["tx_date"],
                    "running_total": int(running_total) if running_total.is_integer() else running_total
                })
                break

    # Sort by account_name alphabetically
    expected_alerts.sort(key=lambda x: x["account_name"])

    expected_lines = [
        f"{alert['account_name']},{alert['tx_date']},{alert['running_total']}"
        for alert in expected_alerts
    ]

    with open(alerts_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {alerts_path} does not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_query_plan_contains_index():
    plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(plan_path), f"Query plan file {plan_path} does not exist."

    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    assert "idx_src_date" in content, (
        f"Query plan in {plan_path} does not indicate usage of 'idx_src_date'."
    )