# test_final_state.py
import os
import csv
import json
import heapq
import pytest

def compute_expected_latency():
    routers_file = "/home/user/data/routers.csv"
    links_file = "/home/user/data/links.csv"

    valid_routers = set()
    with open(routers_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            props = json.loads(row["properties"])
            if props.get("active") is True and props.get("capacity", 0) >= 50:
                valid_routers.add(row["router_id"])

    graph = {r: {} for r in valid_routers}
    with open(links_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row["source"]
            v = row["target"]
            w = int(row["latency_ms"])
            if u in valid_routers and v in valid_routers:
                if v not in graph[u] or w < graph[u][v]:
                    graph[u][v] = w
                if u not in graph[v] or w < graph[v][u]:
                    graph[v][u] = w

    start = "R1"
    end = "R15"
    if start not in valid_routers or end not in valid_routers:
        return -1

    pq = [(0, start)]
    dist = {start: 0}

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')):
            continue
        if u == end:
            return d
        for v, w in graph[u].items():
            if dist.get(v, float('inf')) > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))

    return dist.get(end, -1)

def test_analyze_script_exists():
    assert os.path.isfile("/home/user/analyze.py"), "/home/user/analyze.py does not exist."

def test_answer_file_exists():
    assert os.path.isfile("/home/user/answer.txt"), "/home/user/answer.txt does not exist."

def test_answer_content():
    expected_latency = compute_expected_latency()
    assert expected_latency != -1, "No valid path found between R1 and R15 in the test data."

    expected_string = f"Total Latency: {expected_latency}"

    with open("/home/user/answer.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_string, f"Expected '/home/user/answer.txt' to contain exactly '{expected_string}', but found '{content}'."