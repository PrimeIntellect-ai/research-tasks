# test_final_state.py

import os
import json
import sqlite3
import math

def get_expected_cost(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, parent_id, required_qty, unit_cost FROM components")
    rows = c.fetchall()
    conn.close()

    children = {}
    costs = {}
    qtys = {}
    for cid, pid, qty, cost in rows:
        costs[cid] = cost
        qtys[cid] = qty
        if pid not in children:
            children[pid] = []
        children[pid].append(cid)

    def calculate_cost(cid):
        total = costs[cid]
        for child in children.get(cid, []):
            total += calculate_cost(child) * qtys[child]
        return total

    return calculate_cost(1)

def get_expected_centrality(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, parent_id FROM components")
    rows = c.fetchall()
    conn.close()

    in_degrees = {}
    nodes = set()
    for cid, pid in rows:
        nodes.add(cid)
        if pid is not None:
            nodes.add(pid)
            in_degrees[cid] = in_degrees.get(cid, 0) + 1

    for node in nodes:
        if node not in in_degrees:
            in_degrees[node] = 0

    n = len(nodes)
    if n <= 1:
        centrality = {node: 0 for node in nodes}
    else:
        centrality = {node: deg / (n - 1) for node, deg in in_degrees.items()}

    sorted_nodes = sorted(centrality.keys(), key=lambda x: (-centrality[x], x))
    return sorted_nodes[:2]

def get_expected_capacity(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    capacity = {}
    for supplier in data:
        for item in supplier.get("inventory", []):
            cid = str(item["component_id"])
            capacity[cid] = capacity.get(cid, 0) + item["qty"]

    return capacity

def test_optimization_report_exists():
    report_path = "/home/user/optimization_report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} was not found."

def test_optimization_report_contents():
    report_path = "/home/user/optimization_report.json"
    db_path = "/home/user/supply_chain.db"
    suppliers_path = "/home/user/suppliers.json"

    assert os.path.isfile(report_path), "Report file is missing."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert "total_root_cost" in report, "Missing 'total_root_cost' in the report."
    assert "top_2_central_components" in report, "Missing 'top_2_central_components' in the report."
    assert "total_capacity_by_component" in report, "Missing 'total_capacity_by_component' in the report."

    expected_cost = get_expected_cost(db_path)
    assert math.isclose(report["total_root_cost"], expected_cost, rel_tol=1e-5), \
        f"Expected total_root_cost to be {expected_cost}, but got {report['total_root_cost']}."

    expected_centrality = get_expected_centrality(db_path)
    assert report["top_2_central_components"] == expected_centrality, \
        f"Expected top_2_central_components to be {expected_centrality}, but got {report['top_2_central_components']}."

    expected_capacity = get_expected_capacity(suppliers_path)
    # Convert keys to strings for comparison just in case
    report_capacity = {str(k): v for k, v in report["total_capacity_by_component"].items()}
    assert report_capacity == expected_capacity, \
        f"Expected total_capacity_by_component to be {expected_capacity}, but got {report_capacity}."