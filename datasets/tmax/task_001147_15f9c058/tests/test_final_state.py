# test_final_state.py
import os
import csv
import heapq
import pytest

def compute_expected_results(data_dir):
    edges_csv = os.path.join(data_dir, "edges.csv")
    queries_csv = os.path.join(data_dir, "queries.csv")

    graph = {}
    with open(edges_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row['source_id']
            tgt = row['target_id']
            dist = float(row['distance'])
            cost = float(row['cost'])
            if src not in graph:
                graph[src] = []
            graph[src].append((tgt, dist, cost))
            if tgt not in graph:
                graph[tgt] = []

    queries = []
    with open(queries_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            queries.append((row['source_id'], row['target_id']))

    results = []
    succ_count = 0
    fail_count = 0
    tot_dist = 0.0
    tot_cost = 0.0

    for src, tgt in queries:
        pq = [(0.0, 0.0, src, [src])]
        visited = set()
        found = False

        while pq:
            d, c, u, path = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            if u == tgt:
                results.append((src, tgt, d, c, "-".join(path)))
                succ_count += 1
                tot_dist += d
                tot_cost += c
                found = True
                break

            for v, weight, cost_val in graph.get(u, []):
                if v not in visited:
                    heapq.heappush(pq, (d + weight, c + cost_val, v, path + [v]))

        if not found:
            results.append((src, tgt, -1.0, -1.0, "NONE"))
            fail_count += 1

    return results, succ_count, fail_count, tot_dist, tot_cost

def test_run_script_exists_and_executable():
    script_path = "/home/user/logistics_graph/run.sh"
    assert os.path.isfile(script_path), f"Build and run script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} must be executable."

def test_results_csv_correctness():
    output_csv = "/home/user/logistics_graph/output/results.csv"
    assert os.path.isfile(output_csv), f"Output file {output_csv} is missing."

    data_dir = "/home/user/logistics_graph/data"
    expected_results, _, _, _, _ = compute_expected_results(data_dir)

    actual_results = {}
    with open(output_csv, 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines:
            if line.startswith("source_id"):
                continue
            parts = line.split(',')
            if len(parts) == 5:
                src, tgt, dist, cost, path = parts
                actual_results[(src, tgt)] = (float(dist), float(cost), path)

    for src, tgt, exp_d, exp_c, exp_p in expected_results:
        assert (src, tgt) in actual_results, f"Missing query result for {src} to {tgt}."
        act_d, act_c, act_p = actual_results[(src, tgt)]
        assert abs(act_d - exp_d) < 1e-5, f"Incorrect distance for {src}->{tgt}. Expected {exp_d}, got {act_d}."
        assert abs(act_c - exp_c) < 1e-5, f"Incorrect cost for {src}->{tgt}. Expected {exp_c}, got {act_c}."
        assert act_p == exp_p, f"Incorrect path for {src}->{tgt}. Expected {exp_p}, got {act_p}."

def test_summary_txt_correctness():
    summary_txt = "/home/user/logistics_graph/output/summary.txt"
    assert os.path.isfile(summary_txt), f"Output file {summary_txt} is missing."

    data_dir = "/home/user/logistics_graph/data"
    _, exp_succ, exp_fail, exp_dist, exp_cost = compute_expected_results(data_dir)

    with open(summary_txt, 'r') as f:
        content = f.read()

    assert f"Successful Queries: {exp_succ}" in content, "Incorrect successful queries count."
    assert f"Failed Queries: {exp_fail}" in content, "Incorrect failed queries count."

    # Check floats with 1 decimal place
    exp_dist_str = f"Total Accumulated Distance: {exp_dist:.1f}"
    exp_cost_str = f"Total Accumulated Cost: {exp_cost:.1f}"

    assert exp_dist_str in content, f"Incorrect total distance. Expected '{exp_dist_str}'."
    assert exp_cost_str in content, f"Incorrect total cost. Expected '{exp_cost_str}'."