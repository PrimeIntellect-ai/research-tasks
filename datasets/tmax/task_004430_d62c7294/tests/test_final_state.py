# test_final_state.py

import os
import time
import json
import hashlib
import urllib.request
import urllib.error
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
PROXY_URL = "http://localhost:8080/query"
INDEX_SCRIPT = "/home/user/indexes.cypher"
PROXY_SOURCE = "/home/user/app/proxy.go"

@pytest.fixture(scope="session", autouse=True)
def setup_services_and_proxy():
    # Ensure docker-compose is up
    subprocess.run(["docker-compose", "-f", "/app/docker-compose.yml", "up", "-d"], check=True)

    # Wait for Neo4j to be healthy
    for _ in range(30):
        if subprocess.run(["nc", "-z", "localhost", "7687"]).returncode == 0:
            break
        time.sleep(1)
    else:
        pytest.fail("Neo4j did not become healthy in time.")

    # Apply indexes if the file exists
    if os.path.exists(INDEX_SCRIPT):
        subprocess.run(["cypher-shell", "-u", "neo4j", "-p", "password", "-f", INDEX_SCRIPT], check=False)

    # Start the Go proxy
    if os.path.exists(PROXY_SOURCE):
        proxy_proc = subprocess.Popen(["go", "run", PROXY_SOURCE])
        # Wait for proxy to listen on 8080
        for _ in range(30):
            if subprocess.run(["nc", "-z", "localhost", "8080"]).returncode == 0:
                break
            time.sleep(1)
        else:
            proxy_proc.kill()
            pytest.fail("Go proxy did not start listening on port 8080 in time.")

        yield

        proxy_proc.kill()
    else:
        yield

def test_indexes_created():
    assert os.path.exists(INDEX_SCRIPT), f"{INDEX_SCRIPT} is missing"

    # Check indexes in Neo4j
    result = subprocess.run(
        ["cypher-shell", "-u", "neo4j", "-p", "password", "--format", "plain", "SHOW INDEXES YIELD labelsOrTypes, properties;"],
        capture_output=True, text=True
    )
    output = result.stdout

    # Look for Employee(emp_id) and Department(dept_name)
    assert "Employee" in output and "emp_id" in output, "Index on Employee(emp_id) not found in Neo4j"
    assert "Department" in output and "dept_name" in output, "Index on Department(dept_name) not found in Neo4j"

def test_proxy_exists():
    assert os.path.exists(PROXY_SOURCE), f"{PROXY_SOURCE} is missing"

def test_adversarial_corpus_firewall():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.cypher')]
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.cypher')]

    clean_failed = []
    evil_failed = []

    # Test clean corpus
    for cf in clean_files:
        with open(cf, 'r') as f:
            query = f.read()

        req = urllib.request.Request(PROXY_URL, data=query.encode('utf-8'), method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    clean_failed.append(os.path.basename(cf))
                else:
                    # Check if valid JSON
                    try:
                        json.loads(response.read().decode('utf-8'))
                    except json.JSONDecodeError:
                        clean_failed.append(os.path.basename(cf) + " (invalid JSON)")
        except Exception:
            clean_failed.append(os.path.basename(cf))

    # Test evil corpus
    for ef in evil_files:
        with open(ef, 'r') as f:
            query = f.read()

        req = urllib.request.Request(PROXY_URL, data=query.encode('utf-8'), method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                # If it succeeds, it failed to block
                evil_failed.append(os.path.basename(ef))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_failed.append(os.path.basename(ef) + f" (HTTP {e.code})")
        except Exception:
            evil_failed.append(os.path.basename(ef) + " (Connection error)")

    err_msg = []
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified or rejected: {', '.join(clean_failed)}")

    assert not err_msg, " | ".join(err_msg)

def test_redis_caching():
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.cypher')]

    for cf in clean_files:
        with open(cf, 'r') as f:
            query = f.read()

        query_hash = hashlib.sha256(query.encode('utf-8')).hexdigest()

        # Check Redis for this hash
        # We can use redis-cli via subprocess
        result = subprocess.run(
            ["docker-compose", "-f", "/app/docker-compose.yml", "exec", "-T", "redis", "redis-cli", "EXISTS", query_hash],
            capture_output=True, text=True
        )
        # EXISTS returns 1 if key exists
        assert "1" in result.stdout, f"Query hash {query_hash} for {os.path.basename(cf)} not found in Redis"