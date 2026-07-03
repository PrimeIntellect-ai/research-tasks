# test_final_state.py

import os
import csv
from collections import defaultdict

def get_expected_cycles():
    accounts_file = "/home/user/accounts.csv"
    transactions_file = "/home/user/transactions.csv"

    accounts = {}
    with open(accounts_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            accounts[row["account_id"]] = {
                "created_at": row["created_at"],
                "status": row["status"]
            }

    edges = defaultdict(float)
    graph = defaultdict(set)
    with open(transactions_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["src_account"]
            dst = row["dst_account"]
            amount = float(row["amount"])
            edges[(src, dst)] = max(edges[(src, dst)], amount)
            graph[src].add(dst)

    cycles = set()
    for a in graph:
        for b in graph[a]:
            if b == a:
                continue
            for c in graph[b]:
                if c == a or c == b:
                    continue
                if a in graph[c]:
                    # Found cycle A -> B -> C -> A
                    cycle_nodes = (a, b, c)

                    # Check status
                    if any(accounts[node]["status"] != "ACTIVE" for node in cycle_nodes):
                        continue

                    # Check created_at > 2023-01-01
                    if not any(accounts[node]["created_at"] > "2023-01-01" for node in cycle_nodes):
                        continue

                    # Check volume
                    volume = edges[(a, b)] + edges[(b, c)] + edges[(c, a)]
                    if volume <= 10000.0:
                        continue

                    # Normalize cycle representation
                    normalized_cycle = tuple(sorted(cycle_nodes))
                    cycles.add(normalized_cycle)

    sorted_cycles = sorted(list(cycles))
    return [" ".join(cycle) for cycle in sorted_cycles]

def test_fraud_cycles_log():
    log_file = "/home/user/fraud_cycles.log"
    assert os.path.isfile(log_file), f"The output file {log_file} does not exist."

    with open(log_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = get_expected_cycles()

    assert lines == expected_lines, (
        f"The contents of {log_file} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(lines)}"
    )