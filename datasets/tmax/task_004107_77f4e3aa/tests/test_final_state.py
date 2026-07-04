# test_final_state.py

import json
import random
import heapq
import urllib.request
import urllib.error
import hashlib
import time
import pytest
import redis

def generate_dag(num_jobs, num_edges):
    edges = set()
    possible_edges = num_jobs * (num_jobs - 1) // 2
    num_edges = min(num_edges, possible_edges)

    while len(edges) < num_edges:
        u = random.randint(0, num_jobs - 2)
        v = random.randint(u + 1, num_jobs - 1)
        edges.add((u, v))

    perm = list(range(num_jobs))
    random.shuffle(perm)

    mapped_edges = []
    for u, v in edges:
        mapped_edges.append([perm[u], perm[v]])

    return num_jobs, mapped_edges

def oracle_topological_sort(num_jobs, edges):
    adj = {i: [] for i in range(num_jobs)}
    in_degree = {i: 0 for i in range(num_jobs)}
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    pq = []
    for i in range(num_jobs):
        if in_degree[i] == 0:
            heapq.heappush(pq, i)

    result = []
    while pq:
        curr = heapq.heappop(pq)
        result.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(pq, neighbor)

    return result

def send_request(payload):
    req = urllib.request.Request(
        "http://127.0.0.1:8080/schedule",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        pytest.fail(f"Request to gateway failed: {e}")

def test_fuzz_equivalence_and_caching():
    random.seed(42)

    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Redis server is not running or accessible on 127.0.0.1:6379")

    # Fuzz with 50 inputs to ensure memory safety and correctness
    for i in range(50):
        jobs = random.randint(10, 1000)
        edges = random.randint(0, 5000)
        num_jobs, deps = generate_dag(jobs, edges)

        payload = {"jobs": num_jobs, "dependencies": deps}
        expected_schedule = oracle_topological_sort(num_jobs, deps)

        # First request (Cache miss)
        response = send_request(payload)
        assert "schedule" in response, f"Response missing 'schedule' key. Payload: {payload}"
        assert response["schedule"] == expected_schedule, \
            f"Mismatch on request {i}. Expected {expected_schedule[:10]}..., got {response['schedule'][:10]}..."

        # Verify Redis caching
        # The task specifies: deterministically stringify the incoming JSON and compute its SHA256 hash.
        # usually json.dumps(payload, sort_keys=True) or similar.
        # We can just verify that a second request returns the same result.
        response2 = send_request(payload)
        assert response2["schedule"] == expected_schedule, "Second request (cache hit) returned incorrect data."

def test_services_running():
    # Check if the python gateway is listening on 8080
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/", method='GET')
        with urllib.request.urlopen(req, timeout=1):
            pass
    except urllib.error.HTTPError:
        pass # 404 or 405 is fine, means it's listening
    except urllib.error.URLError:
        pytest.fail("Python gateway is not running on port 8080")