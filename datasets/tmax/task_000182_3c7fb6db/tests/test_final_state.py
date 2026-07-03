# test_final_state.py

import os
import time
import pytest
try:
    from neo4j import GraphDatabase
except ImportError:
    pytest.skip("neo4j driver not installed, cannot run tests", allow_module_level=True)

CYPHER_QUERY_PATH = "/home/user/target_query.cypher"

def test_target_query_exists():
    assert os.path.isfile(CYPHER_QUERY_PATH), f"Target query file is missing at {CYPHER_QUERY_PATH}"

def test_graph_query_correctness_and_performance():
    assert os.path.isfile(CYPHER_QUERY_PATH), f"Missing {CYPHER_QUERY_PATH}"
    with open(CYPHER_QUERY_PATH, "r") as f:
        query = f.read().strip()

    assert query, "The Cypher query file is empty."

    driver = GraphDatabase.driver("bolt://localhost:7687")

    # Warmup and correctness check
    with driver.session() as session:
        result = session.run(query)
        record = result.single()

        assert record is not None, "Query returned no results."

        # Check columns
        keys = record.keys()
        assert "step1" in keys, "Result must contain 'step1' column."
        assert "step2" in keys, "Result must contain 'step2' column."
        assert "step3" in keys, "Result must contain 'step3' column."
        assert "frequency" in keys, "Result must contain 'frequency' column."

        # Check expected sequence
        assert record["step1"] == "home", f"Expected step1='home', got {record['step1']}"
        assert record["step2"] == "search", f"Expected step2='search', got {record['step2']}"
        assert record["step3"] == "checkout", f"Expected step3='checkout', got {record['step3']}"

    # Benchmark
    start = time.time()
    for _ in range(50):
        with driver.session() as session:
            result = session.run(query)
            # consume the result
            _ = result.single()

    duration = (time.time() - start) / 50.0

    driver.close()

    # Assert performance threshold
    assert duration < 0.015, f"Query execution time was {duration:.4f}s per run, which exceeds the 0.015s threshold. Indexes might be missing or the query is not optimized."