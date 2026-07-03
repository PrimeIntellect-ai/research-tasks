# test_final_state.py
import os
import json
import csv
from collections import defaultdict

def compute_expected_results(csv_path):
    transactions = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                'tx_id': int(row['tx_id']),
                'sender': row['sender'],
                'receiver': row['receiver'],
                'amount': float(row['amount'])
            })

    # Build graph
    graph = defaultdict(set)
    degrees = defaultdict(int)

    for tx in transactions:
        u = tx['sender']
        v = tx['receiver']
        graph[u].add(v)
        degrees[u] += 1
        degrees[v] += 1

    # Find 3-cycles
    cycle_accounts = set()
    for u in graph:
        for v in graph[u]:
            for w in graph[v]:
                if u in graph[w]:
                    cycle_accounts.update([u, v, w])

    cycle_accounts_sorted = sorted(list(cycle_accounts))

    # Find highest degree cycle account
    highest_degree_account = None
    max_degree = -1
    for acc in cycle_accounts_sorted:
        if degrees[acc] > max_degree:
            max_degree = degrees[acc]
            highest_degree_account = acc

    # Find top 2 transactions between cycle accounts
    cycle_txs = [tx for tx in transactions if tx['sender'] in cycle_accounts and tx['receiver'] in cycle_accounts]
    cycle_txs_sorted = sorted(cycle_txs, key=lambda x: x['amount'], reverse=True)
    top_cycle_transactions = [tx['tx_id'] for tx in cycle_txs_sorted[:2]]

    return {
        "cycle_accounts": cycle_accounts_sorted,
        "highest_degree_cycle_account": highest_degree_account,
        "top_cycle_transactions": top_cycle_transactions
    }

def test_audit_results_exists():
    assert os.path.isfile('/home/user/audit_results.json'), "The output file /home/user/audit_results.json is missing."

def test_audit_results_content():
    csv_path = '/home/user/transfers.csv'
    assert os.path.isfile(csv_path), f"The input file {csv_path} is missing."

    expected = compute_expected_results(csv_path)

    with open('/home/user/audit_results.json', 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/audit_results.json is not a valid JSON file."

    assert "cycle_accounts" in actual, "Missing 'cycle_accounts' in JSON output."
    assert "highest_degree_cycle_account" in actual, "Missing 'highest_degree_cycle_account' in JSON output."
    assert "top_cycle_transactions" in actual, "Missing 'top_cycle_transactions' in JSON output."

    assert actual["cycle_accounts"] == expected["cycle_accounts"], f"Expected cycle_accounts to be {expected['cycle_accounts']}, but got {actual['cycle_accounts']}."
    assert actual["highest_degree_cycle_account"] == expected["highest_degree_cycle_account"], f"Expected highest_degree_cycle_account to be {expected['highest_degree_cycle_account']}, but got {actual['highest_degree_cycle_account']}."
    assert actual["top_cycle_transactions"] == expected["top_cycle_transactions"], f"Expected top_cycle_transactions to be {expected['top_cycle_transactions']}, but got {actual['top_cycle_transactions']}."