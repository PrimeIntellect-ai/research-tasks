# test_final_state.py

import os
import json
import sqlite3
import re
import pytest

def get_expected_results():
    db_path = '/home/user/financial.db'
    json_path = '/home/user/entities.json'

    with open(json_path, 'r') as f:
        entities = json.load(f)

    high_risk_accounts = {e['account_id'] for e in entities if e.get('high_risk')}

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Get all transactions > 10000
    c.execute("SELECT tx_id, sender_id, receiver_id, amount, timestamp FROM transactions WHERE amount > 10000")
    initial_txs = c.fetchall()

    # Get all transactions
    c.execute("SELECT tx_id, sender_id, receiver_id, amount, timestamp FROM transactions")
    all_txs = c.fetchall()

    # Get account addresses
    c.execute("SELECT id, address_id FROM accounts")
    account_addresses = dict(c.fetchall())

    conn.close()

    results = []

    for itx in initial_txs:
        itx_id, a_id, b_id, i_amt, i_ts = itx

        # Find subsequent txs from B
        for stx in all_txs:
            stx_id, s_sender, c_id, s_amt, s_ts = stx
            if s_sender == b_id and s_ts > i_ts:
                # distinct accounts
                if len({a_id, b_id, c_id}) == 3:
                    # A and C share address
                    addr_a = account_addresses.get(a_id)
                    addr_c = account_addresses.get(c_id)
                    if addr_a is not None and addr_a == addr_c:
                        # At least one is high risk
                        if a_id in high_risk_accounts or b_id in high_risk_accounts or c_id in high_risk_accounts:
                            results.append({
                                "initial_tx_id": itx_id,
                                "subsequent_tx_id": stx_id,
                                "sender_a_id": a_id,
                                "intermediary_b_id": b_id,
                                "receiver_c_id": c_id,
                                "shared_address_id": addr_a
                            })

    results.sort(key=lambda x: x["initial_tx_id"])
    return results

def test_audit_results():
    results_path = '/home/user/audit_results.json'
    assert os.path.exists(results_path), f"Output file {results_path} is missing."
    assert os.path.isfile(results_path), f"Expected {results_path} to be a file."

    with open(results_path, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected_results = get_expected_results()

    assert isinstance(actual_results, list), "Expected the output to be a JSON array."
    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results, found {len(actual_results)}."

    for actual, expected in zip(actual_results, expected_results):
        assert actual == expected, f"Mismatch in output. Expected {expected}, got {actual}."

def test_indexes_sql():
    sql_path = '/home/user/indexes.sql'
    assert os.path.exists(sql_path), f"Indexes file {sql_path} is missing."
    assert os.path.isfile(sql_path), f"Expected {sql_path} to be a file."

    with open(sql_path, 'r') as f:
        content = f.read()

    # Find all CREATE INDEX statements
    create_index_statements = re.findall(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+.*?;', content, re.IGNORECASE | re.DOTALL)

    assert len(create_index_statements) >= 2, "Expected at least 2 CREATE INDEX statements in indexes.sql."

    # Check if they target the expected columns without enforcing exact parsing, just looking for table and column names
    valid_targets = [
        r'transactions\s*\(\s*amount\s*\)',
        r'transactions\s*\(\s*sender_id\s*\)',
        r'transactions\s*\(\s*receiver_id\s*\)',
        r'accounts\s*\(\s*address_id\s*\)'
    ]

    matched_targets = 0
    for stmt in create_index_statements:
        for target in valid_targets:
            if re.search(target, stmt, re.IGNORECASE):
                matched_targets += 1
                break

    assert matched_targets >= 2, "Indexes should target transactions(amount), transactions(sender_id), transactions(receiver_id), or accounts(address_id)."